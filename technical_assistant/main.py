import json
import os

import nltk
import pandas as pd
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from swarm import Swarm

from technical_assistant.agents.agents import Agents

nltk.download('punkt_tab', quiet=True)
model = SentenceTransformer("all-MiniLM-L6-v2")


def data_preprocess():
    try:
        if os.getenv('document_path'):
            with open(os.getenv('document_path'), 'r') as file:
                dataset = json.load(file)
                data_df = pd.DataFrame(dataset['troubleshooting_scenarios'])
                data_df['issue_embedding'] = data_df['issue'].apply(lambda x: model.encode(x).tolist())
                data_df.to_csv(os.getenv('processed_document_path'))

                if os.getenv('processed_document_path'):
                    with open(os.getenv('processed_document_path'), 'w') as processed_file:
                        json.dump(data_df.to_dict(orient='records'), processed_file)
                else:
                    print("Specify processed_document_path in env file")
        else:
            print("Specify document path in env file")
    except FileNotFoundError:
        print("Error in loading data")


def main():
    load_dotenv()
    data_preprocess()
    user_continue = 'Y'
    while user_continue == 'Y' or user_continue == 'y':
        user_query = input(os.getenv('welcome_message'))
        messages = [{"role": "user", "content": user_query}]
        client = Swarm()
        response = client.run(agent=Agents().local_search_agent, messages=messages)
        messages = response.messages[-1]['content']
        print(messages)
        user_continue = input("Do you want to continue (Y/N)?")


if __name__ == '__main__':
    main()
