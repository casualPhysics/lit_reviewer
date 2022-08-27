from dash import Dash, html, Input, Output, dash_table
import pandas as pd
from paper_sort import query_relevant_papers
from semantic_scholar_api import call_semantic_scholar


paper_topic = 'Royal gardens'
query = paper_topic
limit = 10
fields = ['title', 'authors', 'abstract', 'url']
text_field = 'abstract'

texts = call_semantic_scholar(paper_topic, limit, fields)
df = query_relevant_papers(texts, text_field, query).to_csv('test.csv')
df = pd.read_csv('test.csv')


app = Dash(__name__)

app.layout = html.Div([
    html.H4('Simple interactive table'),
    html.P(id='table_out'),
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i}
                 for i in df.columns],
        data=df.to_dict('records'),
        style_cell=dict(textAlign='left'),
        style_header=dict(backgroundColor="paleturquoise"),
        style_data=dict(backgroundColor="lavender")
    ),
])

@app.callback(
    Output('table_out', 'children'),
    Input('table', 'active_cell'))
def update_graphs(active_cell):
    if active_cell:
        cell_data = df.iloc[active_cell['row']][active_cell['column_id']]
        return f"Data: \"{cell_data}\" from table cell: {active_cell}"
    return "Click the table"


if __name__ == "__main__":
    app.run_server(debug=True)
