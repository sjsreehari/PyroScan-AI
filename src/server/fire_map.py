import folium
import csv

# Path to your fire data CSV file
CSV_PATH = 'src/db/fire_data.csv'

# Center of the map (can be set to average or a fixed location)
MAP_CENTER = [50.0, 15.0]
MAP_ZOOM = 5

# Create a folium map with OpenStreetMap tiles for a real-world look
fire_map = folium.Map(
    location=MAP_CENTER,
    zoom_start=MAP_ZOOM,
    tiles='OpenStreetMap'
)

# Read fire data and add markers

# Limit the number of rows to process for speed
MAX_ROWS = 1000

with open(CSV_PATH, newline='') as csvfile:
    reader = csv.reader(csvfile)
    for i, row in enumerate(reader):
        if i >= MAX_ROWS:
            break
        try:
            lat = float(row[0])
            lon = float(row[1])
            brightness = row[2]
            acq_date = row[5]
            acq_time = row[6]
            folium.CircleMarker(
                location=[lat, lon],
                radius=6,
                popup=f"Brightness: {brightness}<br>Date: {acq_date} {acq_time}",
                color='red',
                fill=True,
                fill_color='orange',
                fill_opacity=0.7
            ).add_to(fire_map)
            print(f"Added marker: lat={lat}, lon={lon}, date={acq_date}, time={acq_time}")
        except Exception:
            continue

# Save the map to an HTML file
fire_map.save('fire_map.html')
print('Interactive fire map saved as fire_map.html')
