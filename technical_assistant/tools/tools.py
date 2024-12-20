import json
import pandas as pd
from fuzzywuzzy import fuzz
from sentence_transformers import SentenceTransformer
import os

model = SentenceTransformer("all-MiniLM-L6-v2")


def load_data():
    with open(os.getenv('document_path'), 'r') as file:
        dataset = json.load(file)
        data_df = pd.DataFrame(dataset['troubleshooting_scenarios'])
        data_df['issue_embedding'] = data_df['issue'].apply(lambda x: model.encode(x).tolist())
        return data_df


def get_agents():
    from technical_assistant.agents.agents import Agents
    agent = Agents()
    return agent


def find_matching_issue(user_query):
    data_df = load_data()

    similarity_score = data_df['issue_embedding'].apply(
        lambda x: model.similarity(model.encode(user_query), x).item() * 100.0)
    similarity_score_max_index = similarity_score.idxmax()
    token_matching_score = data_df['issue'].apply(lambda x: fuzz.token_set_ratio(user_query, x))
    token_matching_score_max_index = token_matching_score.idxmax()

    print(similarity_score)
    print(token_matching_score)
    print(similarity_score_max_index)
    print(token_matching_score_max_index)

    if similarity_score[similarity_score_max_index] > float(os.getenv('similarity_threshold')) or token_matching_score[
        token_matching_score_max_index] > float(os.getenv('token_matching_threshold')):
        max_index = similarity_score_max_index if similarity_score[similarity_score_max_index] > token_matching_score[token_matching_score_max_index] else token_matching_score_max_index
        return data_df['steps'][max_index]
    else:
        get_agents().transfer_to_local_search_agent()


def get_result(steps):
    if steps:
        print(steps)
    else:
        get_agents().transfer_to_web_search_agent()
