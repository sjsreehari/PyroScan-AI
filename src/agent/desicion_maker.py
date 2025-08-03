from langchain_openai import ChatOpenAI
import os
import pandas as pd
from src.agent.prompt import PredictFireOccuringPlace
import json


from dotenv import load_dotenv


load_dotenv()

def PredictFirePlaces():
    llm = ChatOpenAI(
        model="deepseek/deepseek-chat-v3-0324:free",
        base_url="https://openrouter.ai/api/v1", 
        api_key=os.getenv("OPENROUTER_API_KEY")
    )

    load_csv = os.path.join("src/db/", "filtered_fire_data.csv")
    save_path = os.path.join("src/db/", "report.ndjson")
    
    
    csv_chunk = pd.read_csv(load_csv)
    csv_data_str = csv_chunk.to_csv(index=False)

    prompt_text = PredictFireOccuringPlace(csv_data_str)

    response = llm.invoke(prompt_text)


    json_str = response.content.strip("```json\n").strip("```")

    fire_trends = json.loads(json_str)[0]


    with open(save_path, "a") as f:
        json.dump(fire_trends, f, indent=2)
        
        
