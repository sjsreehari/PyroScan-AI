# import os
# import cv2
# import numpy as np
# from src.utils.get_cordinates import coordinates
# import json
# from datetime import datetime


# FIREMAP_DIR = os.path.join("src/db", "firemap-storage") 
# LAT_RANGE = 0.1  
# LON_RANGE = 0.1
# save_path = os.path.join("src/db/coordinates_location", "alert.ndjson")

# def find_hotspot(image_path):
#     print("find hotspot on")
#     heatmap = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
#     if heatmap is None:
#         return None
#     min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(heatmap)
#     print("find hotspot off")
#     return max_loc, heatmap.shape, max_val

# def pixel_to_geo(max_loc, shape, center_lat, center_lon):
#     print("pixel function on")
#     x, y = max_loc
#     h, w = shape

#     deg_per_pixel_lat = LAT_RANGE / h
#     deg_per_pixel_lon = LON_RANGE / w

#     top_left_lat = center_lat + LAT_RANGE / 2
#     top_left_lon = center_lon - LON_RANGE / 2

#     lat = top_left_lat - (y * deg_per_pixel_lat)
#     lon = top_left_lon + (x * deg_per_pixel_lon)
#     print("pixel function off")
#     return lat, lon

# def process_all_heatmaps():
#     results = []
#     print("Processing all heatmaps...")

#     with open(save_path, 'a') as f: 
#         for folder in os.listdir(FIREMAP_DIR):
#             folder_path = os.path.join(FIREMAP_DIR, folder)

#             coord = coordinates(folder_path)
#             center_lat = float(coord['lattitude'])
#             center_lon = float(coord['longitude'])

#             for file in os.listdir(folder_path):
#                 if file.endswith('.png'):
#                     image_path = os.path.join(folder_path, file)
#                     result = find_hotspot(image_path)
#                     print(image_path)
#                     if result:
#                         max_loc, shape, max_val = result
#                         hotspot_lat, hotspot_lon = pixel_to_geo(max_loc, shape, center_lat, center_lon)

#                         output = {
#                             "longitude": f"{hotspot_lon:.3f}",
#                             "lattitude": f"{hotspot_lat:.3f}",
#                             "temp": f"{max_val:.1f}", 
#                             "timestamp": datetime.now().isoformat()
#                         }

#                         results.append(output)
#                         f.write(json.dumps(output) + "\n") 

#     print(results)
#     return results
import os
import cv2
import numpy as np
import json
from datetime import datetime
from src.utils.get_cordinates import coordinates

# Constants
FIREMAP_DIR = os.path.join("src/db", "firemap-storage")
LAT_RANGE = 0.1  # Total vertical span in degrees
LON_RANGE = 0.1  # Total horizontal span in degrees
SAVE_PATH = os.path.join("src/db/coordinates_location", "alert.ndjson")
THRESHOLD_INCREASE = 25  # Pixel intensity threshold to consider heat increasing

# Temperature range (educational)
MIN_TEMP = 20.0
MAX_TEMP = 120.0


def find_hotspot(image_path):
    print("[🔥] Finding hotspot in:", image_path)
    color_heatmap = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if color_heatmap is None:
        print(f"[❌] Failed to load image: {image_path}")
        return None

    # Convert color heatmap to grayscale (perceived brightness)
    gray_heatmap = cv2.cvtColor(color_heatmap, cv2.COLOR_BGR2GRAY)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(gray_heatmap)
    return max_loc, gray_heatmap.shape, max_val, gray_heatmap


def pixel_to_geo(max_loc, shape, center_lat, center_lon):
    x, y = max_loc
    h, w = shape

    deg_per_pixel_lat = LAT_RANGE / h
    deg_per_pixel_lon = LON_RANGE / w

    top_left_lat = center_lat + (LAT_RANGE / 2)
    top_left_lon = center_lon - (LON_RANGE / 2)

    lat = top_left_lat - (y * deg_per_pixel_lat)
    lon = top_left_lon + (x * deg_per_pixel_lon)

    return lat, lon


def detect_heat_increase(prev_image, curr_image, shape):
    if prev_image.shape != curr_image.shape:
        return None

    diff = cv2.subtract(curr_image, prev_image)
    increase_mask = diff > THRESHOLD_INCREASE
    num_hotspots = np.sum(increase_mask)

    return diff, increase_mask.astype(np.uint8), num_hotspots


def process_all_heatmaps():
    results = []
    print("[🔍] Scanning all heatmap folders...")

    with open(SAVE_PATH, 'a') as f:
        for folder in os.listdir(FIREMAP_DIR):
            folder_path = os.path.join(FIREMAP_DIR, folder)
            if not os.path.isdir(folder_path):
                continue

            try:
                coord = coordinates(folder_path)
                center_lat = float(coord['lattitude'])
                center_lon = float(coord['longitude'])
            except Exception as e:
                print(f"[⚠️] Skipping folder {folder}: Invalid coordinates. {e}")
                continue

            heatmap_files = sorted([file for file in os.listdir(folder_path) if file.lower().endswith('.png')])
            prev_heatmap = None

            for file in heatmap_files:
                image_path = os.path.join(folder_path, file)
                result = find_hotspot(image_path)
                if result:
                    max_loc, shape, max_val, heatmap = result
                    hotspot_lat, hotspot_lon = pixel_to_geo(max_loc, shape, center_lat, center_lon)

                    # Relative scaling
                    image_min = np.min(heatmap)
                    image_max = np.max(heatmap)
                    if image_max != image_min:
                        relative_intensity = (max_val - image_min) / (image_max - image_min)
                    else:
                        relative_intensity = 1.0  # Avoid division by zero if uniform image

                    temp_celsius = relative_intensity * (MAX_TEMP - MIN_TEMP) + MIN_TEMP

                    output = {
                        "longitude": f"{hotspot_lon:.5f}",
                        "lattitude": f"{hotspot_lat:.5f}",
                        "temp": f"{temp_celsius:.2f}",
                        "timestamp": datetime.utcnow().isoformat(),
                        "source": file,
                        "temp_scale": {
                            "min_intensity_in_image": int(image_min),
                            "max_intensity_in_image": int(image_max),
                            "min_temp_celsius": MIN_TEMP,
                            "max_temp_celsius": MAX_TEMP,
                            "note": "Educational dummy scale based on relative image intensity"
                        }
                    }

                    # Detect heat increase
                    if prev_heatmap is not None:
                        diff_map, mask, count = detect_heat_increase(prev_heatmap, heatmap, shape)
                        output["heat_increase_pixels"] = int(count)

                        if count > 0:
                            ys, xs = np.where(mask)
                            if len(xs) > 0:
                                avg_x = int(np.mean(xs))
                                avg_y = int(np.mean(ys))
                                inc_lat, inc_lon = pixel_to_geo((avg_x, avg_y), shape, center_lat, center_lon)
                                output["heat_increase_center"] = {
                                    "lat": f"{inc_lat:.5f}",
                                    "lon": f"{inc_lon:.5f}"
                                }

                    results.append(output)
                    f.write(json.dumps(output) + "\n")
                    prev_heatmap = heatmap

    print(f"[🏁] Done. Total heatmaps processed: {len(results)}")
    return results
