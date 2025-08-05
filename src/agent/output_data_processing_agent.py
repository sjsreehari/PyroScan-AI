import os
import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from src.agent.prompt import OutputRawDataProcessorPrompt
import re

def final_output_data_processing_agent():
    load_raw_file = os.path.join("src/db/raw", "agent_thought_output_raw.txt")
    save_processed_file = os.path.join("src/db/processed", "prediction.json")

    
    llm = ChatOpenAI(
        model_name="deepseek/deepseek-chat-v3-0324:free",
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
    )

    with open(load_raw_file, "r") as f:
        raw_data = f.read()

    prompt = OutputRawDataProcessorPrompt(raw_data)

    response = llm.invoke([HumanMessage(content=prompt)])
    processed_data = response.content

    
    match = re.search(r'\[.*?\]', processed_data, re.DOTALL)
    if match:
        json_str = match.group(0)
        try:
            processed_json = json.loads(json_str)
            
            
        except Exception as e:
            processed_json = {"error": f"JSON parsing failed: {str(e)}", "raw": json_str}
            
            
    else:
        try:
            processed_json = json.loads(processed_data)
            
        except Exception as e:
            processed_json = {"error": "No JSON array found in output", "raw": processed_data}


    with open(save_processed_file, "w") as f:
        json.dump(processed_json, f, indent=2)

