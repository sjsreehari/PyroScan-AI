import random
import requests
from PIL import Image
from io import BytesIO
import os
from src.utils.unique_id import unique_image_label
import pandas as pd
import os


load_path = os.path.join("src/data", "danger-zone.csv") 


df = pd.read_csv(load_path)

API_KEY = "902029b0-7b4d-4c06-a37d-0c921bd6dfc4"
API_URL = "https://heatmapapi.com/heatmapapiservices/api/createHeatmap"
NUM_POINTS = 50
RADIUS_MILES = 1
WIDTH, HEIGHT = 400, 300

def generate_random_points(center_lat, center_lon, count):
    points = []
    for _ in range(count):
        lat = center_lat + (random.random() - 0.5) / 25
        lon = center_lon + (random.random() - 0.5) / 12
        weight = 1
        points.append((lat, lon, weight))
    return points

def prepare_datapoints_string(points):
    return ",".join(f"{lat},{lon},{weight}" for lat, lon, weight in points)

def create_heatmap(CENTER_LAT, CENTER_LON, name):
    points = generate_random_points(CENTER_LAT, CENTER_LON, NUM_POINTS)
    data_points_str = prepare_datapoints_string(points)

    lats = [lat for lat, _, _ in points]
    lons = [lon for _, lon, _ in points]

    params = {
        "Width": WIDTH,
        "Height": HEIGHT,
        "Lat1": min(lats),
        "Lat2": max(lats),
        "Lon1": min(lons),
        "Lon2": max(lons),
        "DistanceMultiple": 20,
        "UseAverage": False,
        "ColorPalette": "1",
        "DataPoints": data_points_str
    }

    headers = {
        "Content-Type": "application/json",
        "X-Api-Key": API_KEY
    }

    response = requests.post(API_URL, json=params, headers=headers)
    response.raise_for_status()
    data = response.json()

    if 'imageUrl' in data:
        image_url = f"https://heatmapapi.com/hm/{data['imageUrl']}"
        print("Heatmap image URL:", image_url)

        img_resp = requests.get(image_url)
        img_resp.raise_for_status()
        image = Image.open(BytesIO(img_resp.content))
        output_folder = f"src/db/firemap-storage/{CENTER_LAT}-{CENTER_LON}"
            
        os.makedirs(output_folder, exist_ok=True) 

        label = unique_image_label("heatmap_output.png", name)

        
        output_image_path = os.path.join(output_folder, label)
        image.save(output_image_path)
        
        print(f"Heatmap ====> {name} saved successfully to: {output_image_path}")        
    else:
        print("No image URL returned:", data)


for idx, row in df.iterrows():
    region = row.get("Region", f"zone_{idx}".replace("  ", "_"))
    lat = row
    lat = row["Latitude"]
    lon = row["Longitude"]
    create_heatmap(lat, lon, region)