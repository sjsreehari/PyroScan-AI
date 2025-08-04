import os
import requests
from dotenv import load_dotenv
from pydantic import BaseModel


load_dotenv()
class WeatherToolInput(BaseModel):
    lat: float
    lon: float

def get_weather_data_tool(lat: float, lon: float) -> str:
    API_KEY = os.getenv("WEATHERAPI_API_KEY")
    if not API_KEY:
        return "Weather API key not set."

    base_url = "http://api.weatherapi.com/v1/current.json"
    params = {"key": API_KEY, "q": f"{lat},{lon}"}

    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        current = data.get("current", {})
        location = data.get("location", {})
        return (
            f"Weather at ({lat}, {lon}) [{location.get('name', 'Unknown')}]:\n"
            f"Temperature: {current.get('temp_c', 'N/A')} °C\n"
            f"Condition: {current.get('condition', {}).get('text', 'N/A')}\n"
            f"Wind Speed: {current.get('wind_kph', 'N/A')} kph\n"
            f"Humidity: {current.get('humidity', 'N/A')}%\n"
            f"Local Time: {location.get('localtime', 'N/A')}"
        )
    except Exception as e:
        return f"Error fetching weather: {e}"
