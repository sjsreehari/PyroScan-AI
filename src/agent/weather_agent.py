"""
This is the agent that gets weather data
"""

import os
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentType
from pydantic import BaseModel


from src.tools.runnable import get_weather_data_tool 
from src.agent.prompt import weatherPrompt



class WeatherToolInput(BaseModel):
    lat: float
    lon: float


def analyse_the_weather(target_locations):
    
        
    
    tool = [
    Tool(
        name="Weather tool",
        description="Retrieve current weather for latitude and longitude.",
        func=get_weather_data_tool,
        args_schema=WeatherToolInput,
    )
]
    
    llm = ChatOpenAI(
        model="deepseek/deepseek-chat-v3-0324:free",
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY")
    )

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    agent = initialize_agent(
        tools=tool,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        memory=memory,
        verbose=True,
    )

    prompt = "You are a weather agent. For each location, provide input to Weather tool as JSON with keys lat and lon.\n\nLocations:\n"
    for loc in target_locations:
        prompt += f"- lat: {loc['lat']}, lon: {loc['lon']}\n"

    agent.run(prompt)