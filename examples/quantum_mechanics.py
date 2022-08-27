from semantic_scholar_api import call_semantic_scholar
from paper_sort import query_relevant_papers
import logging

logging.basicConfig(level=logging.INFO)

paper_topic = 'Entanglement dynamics of generic quantum states'
query = 'Entanglement dynamics of generic quantum states'
limit = 10
fields = ['title', 'authors', 'abstract', 'url']
text_field = 'abstract'
save_location = f'../loaded_csvs/{query.lower().replace(" ","_")}'

if __name__ == "__main__":

    logging.info(f'Saving query {paper_topic} with {limit} entries to {save_location}')
    texts = call_semantic_scholar(paper_topic, limit, fields)
    query_relevant_papers(texts, text_field, query).to_csv(save_location)
