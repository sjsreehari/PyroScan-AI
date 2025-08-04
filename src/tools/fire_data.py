import requests
import os
import csv
from io import StringIO
from dotenv import load_dotenv

load_dotenv()

def is_near(lat1, lon1, lat2, lon2, tolerance=0.2):
    return abs(lat1 - lat2) <= tolerance and abs(lon1 - lon2) <= tolerance

def fire_data(lat: float, lon: float) -> str:
    
    
    """
    Fetches fire data from NASA FIRMS and filters for points near the given lat/lon.

    Args:
        lat (float): Latitude of interest.
        lon (float): Longitude of interest.

    Returns:
        str: Summary of any nearby fire activity.
    """
    
    
    API_KEY = os.getenv("NASA_FIRM_API_KEY")
    url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{API_KEY}/VIIRS_SNPP_NRT/world/10"

    import time
    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f"[~] Fetching fire data from FIRMS API... (Attempt {attempt+1})")
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            csv_data = StringIO(response.text)
            reader = csv.DictReader(csv_data)

            fire_matches = []
            for row in reader:
                fire_lat = float(row['latitude'])
                fire_lon = float(row['longitude'])
                if is_near(fire_lat, fire_lon, lat, lon):
                    fire_matches.append(row)

            if not fire_matches:
                return "No fire activity detected near this location."

            summary = f"🔥 {len(fire_matches)} fire spot(s) detected near ({lat}, {lon}):\n"
            for match in fire_matches[:5]:
                summary += f"  - Brightness: {match['bright_ti4']}, Confidence: {match['confidence']}, Time: {match['acq_date']} {match['acq_time']}\n"

            return summary
        except requests.exceptions.Timeout:
            print(f"[x] Request timed out on attempt {attempt+1}.")
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            return "[x] FIRMS API request timed out after multiple attempts."
        except requests.exceptions.HTTPError as e:
            return f"[x] HTTP error: {e}"
        except requests.exceptions.RequestException as e:
            print(f"[x] Request failed on attempt {attempt+1}: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            return f"[x] FIRMS API request failed after multiple attempts: {e}"
        except Exception as e:
            return f"⚠ General error: {e}"
