from swarm import Agent

from technical_assistant.prompts.prompt import LOCAL_SEARCH_PROMPT, WEB_SEARCH_PROMPT
from technical_assistant.tools.tools import find_matching_issue, get_result


class Agents:
    def __init__(self):
        self.local_search_agent = Agent(
            name="LocalSearchAgent",
            instructions=LOCAL_SEARCH_PROMPT,
            functions=[find_matching_issue, get_result]
        )

        self.web_search_agent = Agent(
            name="WebSearchAgent",
            instructions=WEB_SEARCH_PROMPT,
            functions=[
                self.transfer_to_local_search_agent
            ])

    def transfer_to_web_search_agent(self):
        return self.web_search_agent

    def transfer_to_local_search_agent(self):
        return self.web_search_agent
