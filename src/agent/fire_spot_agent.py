"""
This is the agent that takes the heatmap from nasa firms api
"""

from src.tools.fire_data import fire_data
import os

def analyse_fire_places(target_locations):
    print("Fire place analysis started.....")
    
    try:
        if isinstance(target_locations, str):
            coords = target_locations.strip().split(',')
            if len(coords) == 2:
                lat = float(coords[0].strip())
                lon = float(coords[1].strip())
                return fire_data(lat, lon)
        
        elif isinstance(target_locations, dict):
            lat = target_locations.get('lat', 0)
            lon = target_locations.get('lon', 0)
            return fire_data(lat, lon)
        
        elif isinstance(target_locations, (list, tuple)) and len(target_locations) >= 2:
            lat = float(target_locations[0])
            lon = float(target_locations[1])
            return fire_data(lat, lon)
            
        else:
            return "Invalid location format provided. Expected format: 'lat,lon' or dict with lat/lon keys"
            
    except Exception as e:
        return f"Error analyzing fire data: {str(e)}"
