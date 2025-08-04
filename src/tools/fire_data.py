# import requests
# import os
# import csv
# from io import StringIO
# from dotenv import load_dotenv


# load_dotenv()



# target_locations = [
#     {"Location": "Amazon Rainforest", "Latitude": -3.4653, "Longitude": -62.2159},
#     {"Location": "California Wildlands", "Latitude": 36.7783, "Longitude": -119.4179},
#     {"Location": "British Columbia", "Latitude": 53.7267, "Longitude": -127.6476},
#     {"Location": "Siberia Forests", "Latitude": 60.0000, "Longitude": 105.0000},
#     {"Location": "Athens Outskirts", "Latitude": 37.9838, "Longitude": 23.7275},
#     {"Location": "Canberra Region", "Latitude": -35.2809, "Longitude": 149.1300},
#     {"Location": "Alberta Forests", "Latitude": 54.0000, "Longitude": -115.0000},
#     {"Location": "Western Cape", "Latitude": -33.9249, "Longitude": 18.4241},
#     {"Location": "Mato Grosso", "Latitude": -12.6819, "Longitude": -55.6896},
#     {"Location": "Los Angeles National Forest", "Latitude": 34.5000, "Longitude": -118.2000},
# ]

# def is_near(lat1, lon1, lat2, lon2, tolerance=0.2):
#     return abs(lat1 - lat2) <= tolerance and abs(lon1 - lon2) <= tolerance

# def get_fire_data():
    
#     API_KEY = os.getenv("NASA_FIRM_API_KEY")
#     url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{API_KEY}/VIIRS_SNPP_NRT/world/10"
#     save_dir = "src/db"
#     save_path = os.path.join(save_dir, "filtered_fire_data.csv")

#     try:
#         print("[~] Fetching fire data from FIRMS API...")
#         response = requests.get(url, timeout=15)
#         response.raise_for_status()

#         os.makedirs(save_dir, exist_ok=True)

#         csv_data = StringIO(response.text)
#         reader = csv.DictReader(csv_data)

#         with open(save_path, "w", newline="", encoding="utf-8") as f:
#             writer = csv.DictWriter(f, fieldnames=reader.fieldnames)
#             writer.writeheader()

#             for row in reader:
#                 fire_lat = float(row['latitude'])
#                 fire_lon = float(row['longitude'])

#                 for location in target_locations:
#                     if is_near(fire_lat, fire_lon, location['Latitude'], location['Longitude']):
#                         writer.writerow(row)
#                         break

#         print("[*] Filtered fire data saved to db/filtered_fire_data.csv")

#     except requests.exceptions.Timeout:
#         print("[x] Request timed out.")
#     except requests.exceptions.HTTPError as e:
#         print(f"[x] HTTP error: {e}")
#     except requests.exceptions.RequestException as e:
#         print(f"[x] Request failed: {e}")
#     except Exception as e:
#         print(f"⚠ General error: {e}")


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

    try:
        print("[~] Fetching fire data from FIRMS API...")
        response = requests.get(url, timeout=15)
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
        return "[x] Request timed out."
    except requests.exceptions.HTTPError as e:
        return f"[x] HTTP error: {e}"
    except requests.exceptions.RequestException as e:
        return f"[x] Request failed: {e}"
    except Exception as e:
        return f"⚠ General error: {e}"
