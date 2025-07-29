import requests
import os


    
    
def get_fire_data():
    """
    Function to fetch and save fire data from the NASA FIRMS API.
    """
    fire = requests.get("https://firms.modaps.eosdis.nasa.gov/api/area/csv/93f4e7690a9c14e23a4e8d0004c6e0be/VIIRS_SNPP_NRT/world/10").text



    save_path = os.path.join("src/db", "fire_data.csv")

    with open(save_path, "w") as f:
        f.write(fire)

    print("Finished writing fire data to db/fire_data.csv......")