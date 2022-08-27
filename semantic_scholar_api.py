import json
from urllib.request import urlopen

import pandas as pd
from ratelimit import limits

from consts import SEMANTIC_SCHOLAR_FIELDS
from rate_limits import SEMANTIC_SCHOLAR_RATE_LIMIT


@limits(calls=SEMANTIC_SCHOLAR_RATE_LIMIT['calls'],
        period=SEMANTIC_SCHOLAR_RATE_LIMIT['period'])
def construct_semantic_query(
        query: str,
        limit: int,
        fields: list,
        remove_stop_words: bool = True
) -> str:
    """
    Constructs a query for the semantic scholar api.
    This is bounded by the free to use rate limits.

    :param query: The topic to query.
    :param limit: How many articles are called.
    :param fields: Fields of interest.
    :param remove_stop_words: Remove common stop words
    :return:
    """
    for field in fields:
        if field not in SEMANTIC_SCHOLAR_FIELDS:
            raise Exception('Field is not contiained in available fields')
    if limit <= 0:
        raise Exception('Limit is negative, need a postive integer')

    query = '+'.join(query.split(' '))
    fields_joined = ','.join(fields)
    return f"http://api.semanticscholar.org/graph/v1/paper/search?query={query}&offset=10&limit={limit}&fields={fields_joined}"


def call_semantic_scholar(
        query: str,
        limit: int,
        fields: list,
        remove_stop_words: bool = True
):
    return send_request(construct_semantic_query(query, limit, fields))


def send_request(query):
    response = urlopen(query)

    if response.status != 200:
        raise Exception('API response: {}'.format(response.status_code))

    elevations = response.read()
    data = json.loads(elevations)
    df = pd.json_normalize(data['data'])
    return df
