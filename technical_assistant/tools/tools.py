import json
import pandas as pd
from fuzzywuzzy import fuzz
from sentence_transformers import SentenceTransformer
import os

model = SentenceTransformer("all-MiniLM-L6-v2")


def load_data():
    try:
        with open(os.getenv('processed_document_path'), 'r') as processed_file:
            processed_data = json.load(processed_file)
            data_df = pd.DataFrame(processed_data)
        return data_df
    except FileNotFoundError:
        print("Error in loading data")


def get_agents():
    from technical_assistant.agents.agents import Agents
    agent = Agents()
    return agent


def find_matching_issue(user_query):
    data_df = load_data()

    try:
        similarity_score = data_df['issue_embedding'].apply(
            lambda x: model.similarity(model.encode(user_query), x).item() * 100.0)
        similarity_score_max_index = similarity_score.idxmax()
        token_matching_score = data_df['issue'].apply(lambda x: fuzz.token_set_ratio(user_query, x))
        token_matching_score_max_index = token_matching_score.idxmax()

        if similarity_score[similarity_score_max_index] > float(os.getenv('similarity_threshold')) or token_matching_score[
            token_matching_score_max_index] > float(os.getenv('token_matching_threshold')):
            max_index = similarity_score_max_index if similarity_score[similarity_score_max_index] > token_matching_score[
                token_matching_score_max_index] else token_matching_score_max_index
            return data_df['steps'][max_index]
        else:
            agent = get_agents()
            if agent:
                agent.transfer_to_local_search_agent()
            else:
                raise Exception("Failed to reach agent")
    except Exception as e:
        print(f"Error occured: {e}")


def get_result(steps):
    if steps:
        print(steps)
    else:
        get_agents().transfer_to_web_search_agent()
