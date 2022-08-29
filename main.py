from dash import Dash, html, Input, Output, dash_table
import pandas as pd
from paper_sort import query_relevant_papers
from semantic_scholar_api import call_semantic_scholar
from data_preprocessing import truncate_columns


def call_query(

):
    """
    Outputs a
    :return:
    """
    paper_topic = 'Clifford symmetry algebras'
    query = paper_topic
    limit = 40
    fields = ['title', 'authors', 'abstract', 'url']
    text_field = 'abstract'
    texts = call_semantic_scholar(paper_topic, limit, fields)

    return query_relevant_papers(texts, text_field, query).to_csv('tmp.csv')


def call_summary_table(
    df : pd.DataFrame,
    exposed_fields : tuple = ('title', 'abstract', 'url')
):
    summarized = truncate_columns(df)
    summarized = summarized[list(exposed_fields)]
    return df, summarized


# this guy is being called twice
df = pd.read_csv('tmp.csv')
df, summary_df = call_summary_table(df)


app = Dash(__name__)

app.layout = html.Div([
    html.H4('Simple interactive table'),
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i}
                 for i in summary_df.columns],
        data=summary_df.to_dict('records'),
        style_cell=dict(textAlign='left'),
        style_header=dict(backgroundColor="paleturquoise"),
        style_data=dict(backgroundColor="lavender")
    ),
    html.P(id='table_out'),
])

@app.callback(
    Output('table_out', 'children'),
    Input('table', 'active_cell'))
def update_graphs(
        active_cell,
):
    """
    Retrive summary and detail data
    :param active_cell:
    :param summary_df:
    :param detail_df:
    :return:
    """
    if active_cell:
        cell_data = df.iloc[active_cell['row']]['abstract']
        print(cell_data)
        return f"Data: \"{cell_data}\" from table cell: {active_cell}"
    return "Click the table"


if __name__ == "__main__":

    print('test')

    app.run_server(debug=True)
