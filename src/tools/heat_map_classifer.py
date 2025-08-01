import os
import cv2
import numpy as np
from src.utils.get_cordinates import coordinates
import json
from datetime import datetime


FIREMAP_DIR = os.path.join("src/db", "firemap-storage") 
LAT_RANGE = 0.1  
LON_RANGE = 0.1
save_path = os.path.join("src/db/coordinates_location", "alert.ndjson")

def find_hotspot(image_path):
    print("find hotspot on")
    heatmap = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if heatmap is None:
        return None
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(heatmap)
    print("find hotspot off")
    return max_loc, heatmap.shape, max_val

def pixel_to_geo(max_loc, shape, center_lat, center_lon):
    print("pixel function on")
    x, y = max_loc
    h, w = shape

    deg_per_pixel_lat = LAT_RANGE / h
    deg_per_pixel_lon = LON_RANGE / w

    top_left_lat = center_lat + LAT_RANGE / 2
    top_left_lon = center_lon - LON_RANGE / 2

    lat = top_left_lat - (y * deg_per_pixel_lat)
    lon = top_left_lon + (x * deg_per_pixel_lon)
    print("pixel function off")
    return lat, lon

def process_all_heatmaps():
    results = []
    print("Processing all heatmaps...")

    with open(save_path, 'a') as f: 
        for folder in os.listdir(FIREMAP_DIR):
            folder_path = os.path.join(FIREMAP_DIR, folder)

            coord = coordinates(folder_path)
            center_lat = float(coord['lattitude'])
            center_lon = float(coord['longitude'])

            for file in os.listdir(folder_path):
                if file.endswith('.png'):
                    image_path = os.path.join(folder_path, file)
                    result = find_hotspot(image_path)
                    print(image_path)
                    if result:
                        max_loc, shape, max_val = result
                        hotspot_lat, hotspot_lon = pixel_to_geo(max_loc, shape, center_lat, center_lon)

                        output = {
                            "longitude": f"{hotspot_lon:.3f}",
                            "lattitude": f"{hotspot_lat:.3f}",
                            "temp": f"{max_val:.1f}", 
                            "timestamp": datetime.now().isoformat()
                        }

                        results.append(output)
                        f.write(json.dumps(output) + "\n") 

    print(results)
    return results
