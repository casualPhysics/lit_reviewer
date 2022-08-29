"""
Sort through the papers according to query
relevance,  using openai's babbage model.
"""

import openai
import pandas as pd
import tqdm
from openai.embeddings_utils import get_embedding, cosine_similarity
from ratelimit import limits, RateLimitException
import logging
from backoff import on_exception, expo
from params.rate_limits import OPENAI_RATE_LIMIT
import os
from keys import OPENAI_KEY

pd.options.mode.chained_assignment = None
openai.api_key = OPENAI_KEY


@on_exception(expo, RateLimitException, max_tries=8)
@limits(calls=OPENAI_RATE_LIMIT['calls'], period=OPENAI_RATE_LIMIT['period'])
def _get_embedding(
        text : str,
        max_token_length : int = 1000,
        model="text-similarity-davinci-001"
):
    """
    A function that calls an embedding model on some text.
    :param text: Text to embed.
    :param model: Choice of model
    :return: Vector of similarites
    """
    text = text.replace("\n", " ")
    print(len(text) / 4)
    if len(text) / 4  > max_token_length:
        text = text[:max_token_length * 4]
        print('Shortening! ')
    return openai.Embedding.create(input=[text], model=model)['data'][0]['embedding']


def aggregate_columns(df, test_amount):
    df['combined'] = df['title'] + ' ' + df['abstract']
    df = df.dropna(subset=['combined'])[:test_amount]
    return df


@limits(calls=OPENAI_RATE_LIMIT['calls'], period=OPENAI_RATE_LIMIT['period'])
def _attach_text_embeddings(
        df: pd.DataFrame,
        text_field: str = 'combined',
        embedding_model: str = 'text-search-babbage-doc-001',
        embedding_column_name : str = 'search_babbage'
) -> pd.DataFrame:
    """
    Attach embeddings on a dataframe of text.
    :param df: The dataframe in question
    :param text_field: The text field to embed on
    :param embedding_model: The embedding model
    :return:
    """
    logging.info(f"Dropping null columns in {text_field}")
    if text_field not in df.columns: raise Exception('Text field does not exist')

    df = df.dropna(subset=[text_field])
    if len(df) == 0: raise Exception('Length of dataframe is zero after cleaning')

    logging.info(f"Generating embeddings for {len(df)} columns")
    search_babbage = []
    for i in tqdm.tqdm(df[text_field].values):
        search_babbage.append(_get_embedding(i, model=embedding_model))

    df.loc[:, embedding_column_name] = search_babbage
    return df


@limits(calls=OPENAI_RATE_LIMIT['calls'], period=OPENAI_RATE_LIMIT['period'])
def _search_text_from_embeddings(
        df : pd.DataFrame,
        search_query : str,
        embedding_column_name : str = 'search_babbage',
        sim_column_name : str = 'similarities',

) -> pd.DataFrame:

    embedding = _get_embedding(
        search_query,
        model="text-search-babbage-query-001")

    if embedding_column_name not in df.columns:
        raise Exception('No embeddings contained in dataframe - have these been generated?')
    df.loc[:, sim_column_name] = df.search_babbage.apply(lambda x: cosine_similarity(x, embedding))
    return df.sort_values(sim_column_name, ascending=False)


def query_relevant_papers(
        df: pd.DataFrame,
        text_field: str,
        query: str
) -> pd.DataFrame:
    """
    The function exposed to the user.
    Returns a sorted dataFrame of text that match the query.

    :param df: Input Dataframe
    :param text_field: The text in the dataframe
    :param query: The query to sort on
    :return:
    """
    logging.info(f'Ranking topics from {text_field} with query {query}')
    return _search_text_from_embeddings(_attach_text_embeddings(df, text_field), query)
