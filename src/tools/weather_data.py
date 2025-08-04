import requests
import os
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

    try:
        print("[~] Fetching weather data...")
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

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

    except requests.exceptions.Timeout:
        return "[x] Request timed out."
    except requests.exceptions.HTTPError as e:
        return f"[x] HTTP error: {e}"
    except requests.exceptions.RequestException as e:
        return f"[x] Request failed: {e}"
    except Exception as e:
        return f"⚠ General error: {e}"
