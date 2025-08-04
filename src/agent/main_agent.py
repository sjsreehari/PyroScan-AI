"""

This is the main Agent that takes care of all the other agents 

"""


from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentType, Tool
from langchain.callbacks.base import BaseCallbackHandler
from langchain_core.agents import AgentAction, AgentFinish


import os
import json
from dotenv import load_dotenv


from src.agent.prompt import mainPrompt
from src.agent.fire_spot_agent import analyse_fire_places
from src.agent.weather_agent import analyse_the_weather
from src.agent.web_search_agent import analyse_historical_data
from src.agent.output_data_processing_agent import final_output_data_processing_agent

load_dotenv()



class ToolOutputLogger(BaseCallbackHandler):
    def __init__(self):
        self.tool_outputs = []

    def on_tool_end(self, tool_output: str, **kwargs):
        self.tool_outputs.append(tool_output)

    def get_tool_outputs(self):
        return self.tool_outputs


class ReasoningCaptureCallback(BaseCallbackHandler):
    def __init__(self):
        self.logs = []

    def on_llm_new_token(self, token: str, **kwargs):
        self.logs.append(token)

    def on_agent_action(self, action: AgentAction, **kwargs):
        self.logs.append(
            f"\nAgent Action: Tool='{action.tool}', Input='{action.tool_input}', Log='{action.log}'"
        )

    def on_tool_end(self, output: str, **kwargs):
        self.logs.append(f"\nTool Result: {output}")

    def on_agent_finish(self, finish: AgentFinish, **kwargs):
        self.logs.append(
            f"\nAgent Final Answer: {finish.return_values.get('output', 'No final output')}"
        )

    def get_logs(self):
        return "".join(self.logs)



def main_agent():
    
    load_data_file = os.path.join("src/data/", "danger-zone.json")

    
    save_file = os.path.join("src/db/raw", "agent_thought_output_raw.txt")

     
    try:
        llm = ChatOpenAI(
            model="deepseek/deepseek-chat-v3-0324:free",
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY")
        )
    except Exception as e:
        print(f"Warning: OpenRouter failed, trying OpenAI: {e}")
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            api_key=os.getenv("OPENAI_API_KEY")
        )




    fire_agent = [
        Tool(
            name="Fire data extractor",
            description="Use this tool to get the current heatmap data of places using longitude and latitude. Input should be a string with format 'lat,lon' or coordinates separated by comma.",
            func=analyse_fire_places
        )
    ]
    
    weather_agent = [
        Tool(
            name="Weather tool",
            description="Use this tool to get the climate and weather info of a place using the latitude and longitude. Input should be a string with format 'lat,lon' or coordinates separated by comma.",
            func=analyse_the_weather
        )
    ]
    
    websearch_agent = [
        Tool(
            name="Websearch tool",
            description="Use this tool to get the historic weather and disaster conditions of a place using the place name. Input should be a string with the location name.",
            func=analyse_historical_data
        )
    ]
    
    
    tools = fire_agent + weather_agent + websearch_agent


    reasoning_logger = ReasoningCaptureCallback()
    tool_logger = ToolOutputLogger()
    
    
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    
    
    
    agent = initialize_agent(
        tools=tools,
        llm = llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        callbacks=[tool_logger, reasoning_logger],
        memory=memory,
        handle_parsing_errors=True,  

    )
    
    
    
    
    with open(load_data_file, "r", encoding="utf-8") as f:
        location = json.load(f)
    
    
    
    
    
    agent.run(mainPrompt(location))
    
    
    
    with open(save_file, "w", encoding="utf-8") as f:
        f.write("=== AGENT LOGIC & TOOL OUTPUTS ===\n\n")
        f.write(reasoning_logger.get_logs())
        f.write("\n\n=== TOOL RAW OUTPUTS ===\n\n")
        for output in tool_logger.get_tool_outputs():
            f.write(output + "\n\n")

    print(f"[*] Reasoning log saved to: {save_file}")
    
    final_output_data_processing_agent()