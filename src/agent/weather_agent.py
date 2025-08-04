from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentType


from src.tools.runnable import get_weather_data_tool
from src.agent.prompt import weatherPrompt
import os


def analyse_the_weather(target_locations):
    
    print("weather place analysis started.....")

      
    llm = ChatOpenAI(
        model="deepseek/deepseek-chat-v3-0324:free",
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY")
    )


    tool = [
        Tool(
            name="Fire data",
            description="""
                        Retrieves current or forecasted weather data for given latitude and longitude.

                        Args:
                            lat (float): Latitude of the location.
                            lon (float): Longitude of the location.

                        Returns:
                            str: Weather data for the location.
                        """,
            func=get_weather_data_tool
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
    
    
    agent.run(weatherPrompt(target_locations))
