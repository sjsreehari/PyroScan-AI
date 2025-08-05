import requests
import os
import time
from dotenv import load_dotenv


load_dotenv()

def weather_data(lat: float, lon: float) -> str:
    
    
    """
    Fetches current weather data from WeatherAPI for given lat/lon.

    Args:
        lat (float): Latitude of interest.
        lon (float): Longitude of interest.

    Returns:
        str: Summary of current weather conditions.
    """
    
    
    
    API_KEY = os.getenv("WEATHERAPI_API_KEY")
    if not API_KEY:
        return "Weather API key not set."




    base_url = "http://api.weatherapi.com/v1/current.json"
    params = {
        "key": API_KEY,
        "q": f"{lat},{lon}"
    }

    
    max_retries = 3
    for attempt in range(max_retries):
        
        try:
            print(f"[~] Fetching weather data... (Attempt {attempt+1})")
            response = requests.get(base_url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            break
        
        
        except requests.exceptions.Timeout:
            print(f"[x] WeatherAPI request timed out on attempt {attempt+1}.")
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            return "WeatherAPI request timed out after multiple attempts."
        
        
        except requests.exceptions.RequestException as e:
            print(f"[x] WeatherAPI request failed on attempt {attempt+1}: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            return f"WeatherAPI request failed after multiple attempts: {e}"


    if 'data' not in locals():
        return "WeatherAPI failed to return data."

    current = data.get("current", {})
    location = data.get("location", {})


    temp_c = current.get("temp_c", "N/A")
    condition = current.get("condition", {}).get("text", "N/A")
    wind_kph = current.get("wind_kph", "N/A")
    humidity = current.get("humidity", "N/A")
    local_time = location.get("localtime", "N/A")



    summary = (
        f"Weather at ({lat}, {lon}) [{location.get('name', 'Unknown')}]:\n"
        f"Temperature: {temp_c} °C\n"
        f"Condition: {condition}\n"
        f"Wind Speed: {wind_kph} kph\n"
        f"Humidity: {humidity}%\n"
        f"Local Time: {local_time}"
    )
    
    
    return summary
