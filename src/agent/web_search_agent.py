from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool

import os
from dotenv import load_dotenv
from src.tools.runnable import go_websearch_tool
from src.agent.prompt import goWebSearchPrompt

load_dotenv()

def analyse_historical_data(target_locations_name):
    print("Searching the place.....")



    llm = ChatOpenAI(
        model="deepseek/deepseek-chat-v3-0324:free",
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY")
    )




    tool = [
        Tool(
            name="Fire data",
            description=    """
                            Performs a live web search for the given location and returns top results.

                            Args:
                                location (str): The search location.

                            Returns:
                                str: Web search results in a summarized string format.
                            """,
            func=go_websearch_tool
        )
    ]
    
    

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    agent = initialize_agent(
        tools=tool,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        memory=memory,
        verbose=True
    )


    agent.run(goWebSearchPrompt(target_locations_name))