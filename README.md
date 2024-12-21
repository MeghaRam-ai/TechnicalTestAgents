

# Technical Assistant

This is a multi_agent AI based customer support service designed to help with troubleshooting technical problems such as Wi-Fi issue, internet connection problems etc.

Application employs two interconnected agents to deliver optimal step-by-step instructions to the user to solve the technical issues.
Agent1(LocalSearchAgent) interact directly with the user and consult Agent2(WebSearchAgent) if the solution cannot be found using local data.
Agent2 performs a websearch and give back the result to Agent1, which relays to the user.

Currently, the application is limited to commandline execution

## Technologies used:

- **Swarm** : A light-weight multi-agent LLM framework.
- **Sentence-transformers** : To evaluate semantic similarity and also for encoding.
- **FuzzyWuzzy** : To evaluate token/keywords matching



## Installation and running the application

### Environment configuration
Execution depends on the environment variables such as `document_path`, `processed_document_path`,
`SIMILARITY_THRESHOLD`, `TOKEN_MATCHING_THRESHOLD`, and `OPENAI_API_KEY`. These needs to be set before running.

### Install dependencies

- **Install poetry** if not already installed

    ``pip install poetry``


Need to have python 3.12 installed.

    poetry env use <path-to-python3 executable>

    poetry shell


- **Install project dependencies**
    
    `poetry install`


### Run the application

    python technical_assistant/main.py 


## Assumptions Made (More like results from running experiments)

Semantic similarity threshold is set to 90 and token matching threshold is set to 80, a bit less.
For less complex phrases, fuzzy matching can result in high scores around 80 when semantic similarity score are way lesser.
Threshold can be adjusted depending upon the dataset. 

