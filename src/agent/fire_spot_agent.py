"""
This is the agent that takes the heatmap from nasa firms api

"""


from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool

import os
from dotenv import load_dotenv
from src.tools.runnable import get_fire_data_tool
from src.agent.prompt import PredictFireOccuringPlace

load_dotenv()



def analyse_fire_places(target_locations):
    print("Fire place analysis started.....")
    
    llm = ChatOpenAI(
        model="deepseek/deepseek-chat-v3-0324:free",
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY")
    )




    tool = [
        Tool(
            name="Fire data",
            description="""
                        Retrieves recent fire data from NASA FIRMS API for given latitude and longitude.

                        Args:
                            lat (float): Latitude of the location.
                            lon (float): Longitude of the location.

                        Returns:
                            str: Fire activity data for the region.
                        """,
            func=get_fire_data_tool
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


    agent.run(PredictFireOccuringPlace(target_locations))
