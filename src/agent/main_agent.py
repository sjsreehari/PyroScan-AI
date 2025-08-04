# from langchain_openai import ChatOpenAI
# import os
# import pandas as pd
# from src.agent.prompt import PredictFireOccuringPlace
# import json


# from dotenv import load_dotenv


# load_dotenv()

# def PredictFirePlaces():
#     llm = ChatOpenAI(
#         model="deepseek/deepseek-chat-v3-0324:free",
#         base_url="https://openrouter.ai/api/v1", 
#         api_key=os.getenv("OPENROUTER_API_KEY")
#     )

#     load_csv = os.path.join("src/db/", "filtered_fire_data.csv")
#     save_path = os.path.join("src/db/", "report.ndjson")
    
    
#     csv_chunk = pd.read_csv(load_csv)
#     csv_data_str = csv_chunk.to_csv(index=False)

#     prompt_text = PredictFireOccuringPlace(csv_data_str)
#     print(prompt_text)
#     response = llm.invoke(prompt_text)


#     json_str = response.content.strip("```json\n").strip("```")

#     fire_trends = json.loads(json_str)[0]


#     with open(save_path, "a") as f:
#         json.dump(fire_trends, f, indent=2)
        
        
"""

This is the main Agent that takes care of all the other agents 

"""


from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentType, Tool

import os
from dotenv import load_dotenv
from src.agent.prompt import mainPrompt



from src.agent.fire_spot_agent import analyse_fire_places
from src.agent.weather_agent import analyse_the_weather
from src.agent.web_search_agent import analyse_historical_data

load_dotenv()




def main_agent():
    
    
     
    llm = ChatOpenAI(
        model="deepseek/deepseek-chat-v3-0324:free",
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY")
    )




    fire_agent = [
        Tool(
            name="Fire data extractor",
            description="fire_agent Use this tools to get the current heatmap data of this places using the longitude and latitude",
            func=analyse_fire_places
        )
    ]
    
    
    
    
    weather_agent = [
        Tool(
            name="Fire data",
            description="weather_agent Use this tool to get the Climate and weather info of a place using the latitude and longitude",
            func=analyse_the_weather
        )
    ]
    
    
    
    websearch_agent = [
        Tool(
            name="Fire data",
            description="websearch_agent Use this tool to get the historic weather and disaster contition of a place using the place name",
            func=analyse_historical_data
        )
    ]
    
    
    tools = fire_agent + weather_agent + websearch_agent

    
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    
    
    
    agent = initialize_agent(
        tools=tools,
        llm = llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        memory=memory,
        handle_parsing_errors=True,  

    )
    
    
    
    
    location = [    
                {"Location": "Amazon Rainforest", "Latitude": -3.4653, "Longitude": -62.2159},
                {"Location": "California Wildlands", "Latitude": 36.7783, "Longitude": -119.4179},
                {"Location": "British Columbia", "Latitude": 53.7267, "Longitude": -127.6476},
                {"Location": "Siberia Forests", "Latitude": 60.0000, "Longitude": 105.0000},
                {"Location": "Athens Outskirts", "Latitude": 37.9838, "Longitude": 23.7275},
                {"Location": "Canberra Region", "Latitude": -35.2809, "Longitude": 149.1300},
                {"Location": "Alberta Forests", "Latitude": 54.0000, "Longitude": -115.0000},
                {"Location": "Western Cape", "Latitude": -33.9249, "Longitude": 18.4241},
                {"Location": "Mato Grosso", "Latitude": -12.6819, "Longitude": -55.6896},
                {"Location": "Los Angeles National Forest", "Latitude": 34.5000, "Longitude": -118.2000},
            ]
    
    
    
    agent.run(mainPrompt(location))