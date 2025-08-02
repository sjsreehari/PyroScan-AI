import pandas as pd
import csv
from geopy.distance import geodesic

def get_fire_data_by_location():
    print("📍 Enter coordinates to search nearby fire incidents:")
    try:
        lat = float(input("Enter Latitude (e.g., 8.5): "))
        lon = float(input("Enter Longitude (e.g., 76.9): "))
    except ValueError:
        print("❌ Invalid input. Please enter valid numbers.")
        return

    print("⏳ Fetching fire data near your location...")

    # Load full fire dataset
    try:
        file_path = 'src/db/fire_data.csv'  # Path to your full fire dataset
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print("❌ fire_data.csv file not found.")
        return

    # Drop rows with missing lat/lon
    df = df.dropna(subset=['latitude', 'longitude'])

    # Calculate distances
    df['distance_km'] = df.apply(
        lambda row: geodesic((lat, lon), (row['latitude'], row['longitude'])).km,
        axis=1
    )

    # Get nearest row
    nearest_row = df.loc[df['distance_km'].idxmin()]

    # Save to output CSV
    save_path = 'src/db/fire_data_location.csv'
    required_columns = ['latitude', 'longitude', 'acq_date', 'acq_time', 'frp', 'confidence']

    try:
        with open(save_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=required_columns)
            writer.writeheader()
            writer.writerow({col: nearest_row[col] for col in required_columns})
        print(f"✅ Data saved to {save_path}")
        print(f"📍 Nearest fire data is {nearest_row['distance_km']:.2f} km away")
    except Exception as e:
        print(f"❌ Error writing to CSV: {e}")


def menu():
    while True:
        print("\n🔥 PyroScan AI - Fire Data Lookup 🔥")
        print("1. Search fire data by coordinates")
        print("2. Exit")
        choice = input("Enter your choice (1 or 2): ")

        if choice == "1":
            get_fire_data_by_location()
        elif choice == "2":
            print("👋 Exiting. Stay safe!")
            break
        else:
            print("❌ Invalid choice. Please enter 1 or 2.")

