import os

import nltk
from dotenv import load_dotenv
from swarm import Swarm

from technical_assistant.agents.agents import Agents
nltk.download('punkt_tab', quiet=True)


def main():
    load_dotenv()
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
