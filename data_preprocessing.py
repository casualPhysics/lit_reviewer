import pandas as pd 


def shorten_long_strings(
    text : str,
    words_to_truncate = 6
) -> str:
    """
    Strings in tables can be too long
    :param words_to_truncate: How many words we have to reduce this to.
    :return:
    """
    return ' '.join(text.split(' ')[:words_to_truncate]) + ' ...'


def truncate_columns(
    df : pd.DataFrame,
    columns_to_truncate : tuple = ('abstract', )
) -> pd.DataFrame:
    """
    Truncate columns where the text is too much.
    :return: cleaned dataframe with shortened columns
    """
    df = df.copy()
    for col in list(columns_to_truncate):
        if pd.api.types.is_string_dtype(df[col].dtype):
            df[col] = df[col].apply(shorten_long_strings)
        else:
            raise Exception('Column is not of string dtype!')
    return df


def df_preprocessing(
    df : pd.DataFrame,
    columns_of_interest : tuple = (
            'paperId',
            'url',
            'title',
            'abstract',
            'authors',
            'search_babbage',
            'similarities'
    )
):
    """
    We return a dataframe which is simplified.
    :param df:
    :param columns_of_interest:
    :return
    """
    df = df.copy()
    df = df.loc[:, list(columns_of_interest)]
    for col in df.columns:

        if pd.api.types.is_string_dtype(df[col].dtype):
            df[col] = df[col].apply()

    return df
