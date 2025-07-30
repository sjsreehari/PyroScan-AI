# import os
# import pandas as pd
# import math

# df = pd.read_csv(os.path.join("src/db", "fire_data.csv"))

# place = input("Enter a place to check for fire data (latitude,longitude): ")
# try:
#     user_lat, user_lon = map(float, place.split(","))
# except ValueError:
#     print("Invalid input. Use format: latitude,longitude")
#     exit()

# def haversine(lat1, lon1, lat2, lon2):
#     R = 6371  # Earth radius in km
#     dlat = math.radians(lat2 - lat1)
#     dlon = math.radians(lon2 - lon1)
#     a = (math.sin(dlat / 2) ** 2 +
#          math.cos(math.radians(lat1)) *
#          math.cos(math.radians(lat2)) *
#          math.sin(dlon / 2) ** 2)
#     c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
#     return R * c  

# fire_points = df[df["bright_ti4"] > 320]

# fire_points["distance"] = fire_points.apply(
#     lambda row: haversine(user_lat, user_lon, row["latitude"], row["longitude"]),
#     axis=1
# )

# if fire_points.empty:
#     print("No active fire detected nearby.")
# else:
#     nearest_fire = fire_points.loc[fire_points["distance"].idxmin()]
#     print(f"\n🔥 Nearest Fire Detected 🔥")
#     print(f"Location: ({nearest_fire['latitude']}, {nearest_fire['longitude']})")
#     print(f"Brightness: {nearest_fire['bright_ti4']}")
#     print(f"Distance: {nearest_fire['distance']:.2f} km")


from src.tools.fire_data import create_heatmap
create_heatmap()