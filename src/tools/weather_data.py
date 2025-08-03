import requests
import os
import csv
from dotenv import load_dotenv

load_dotenv()

target_locations = [
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

def get_weather_data():
    print("Fetching weather data for target locations...")
    API_KEY = os.getenv("WEATHERAPI_API_KEY")  
    base_url = "http://api.weatherapi.com/v1/current.json"

    save_dir = "src/db"
    save_path = os.path.join(save_dir, "target_locations_weather.csv")

    fieldnames = [
        "Location",
        "Latitude",
        "Longitude",
        "Temperature_C",
        "Condition",
        "Wind_kph",
        "Humidity",
        "Local_Time"
    ]

    os.makedirs(save_dir, exist_ok=True)

    with open(save_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for loc in target_locations:
            lat = loc["Latitude"]
            lon = loc["Longitude"]
            location_name = loc["Location"]

            query = f"{lat},{lon}"
            params = {
                "key": API_KEY,
                "q": query,
            }

            try:
                response = requests.get(base_url, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()

                current = data.get("current", {})
                location_info = data.get("location", {})

                row = {
                    "Location": location_name,
                    "Latitude": lat,
                    "Longitude": lon,
                    "Temperature_C": current.get("temp_c"),
                    "Condition": current.get("condition", {}).get("text"),
                    "Wind_kph": current.get("wind_kph"),
                    "Humidity": current.get("humidity"),
                    "Local_Time": location_info.get("localtime"),
                }

                print(f"Fetched weather for {location_name}: {row['Temperature_C']}°C, {row['Condition']}")
                writer.writerow(row)

            except requests.exceptions.Timeout:
                print(f"[x] Request timed out for {location_name}.")
            except requests.exceptions.HTTPError as e:
                print(f"[x] HTTP error for {location_name}: {e}")
            except requests.exceptions.RequestException as e:
                print(f"[x] Request failed for {location_name}: {e}")
            except Exception as e:
                print(f"⚠ General error for {location_name}: {e}")

    print(f"[*] Weather data saved to {save_path}")
