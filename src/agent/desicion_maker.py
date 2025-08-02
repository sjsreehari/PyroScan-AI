from langchain_openai import ChatOpenAI
import os
import pandas as pd
from src.agent.prompt import PredictFireOccuringPlace


def PredictFirePlaces():
    llm = ChatOpenAI(
        model="deepseek/deepseek-chat-v3-0324:free",
        base_url="https://openrouter.ai/api/v1", 
        api_key="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"  
    )

    load_csv = os.path.join("src/db/", "filtered_fire_data.csv")
    csv_chunk = pd.read_csv(load_csv)
    csv_data_str = csv_chunk.to_csv(index=False)

    prompt_text = PredictFireOccuringPlace(csv_data_str)

    response = llm.invoke(prompt_text)

    print(response)
