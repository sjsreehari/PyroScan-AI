"""
This is the agent that gets weather data
"""

from src.tools.weather_data import weather_data
import os

def analyse_the_weather(target_locations):
    print("weather place analysis started.....")
    
    try:
        # Handle different input formats
        if isinstance(target_locations, str):
            # Parse coordinates from string format "lat,lon"
            coords = target_locations.strip().split(',')
            if len(coords) == 2:
                lat = float(coords[0].strip())
                lon = float(coords[1].strip())
                return weather_data(lat, lon)
        
        elif isinstance(target_locations, dict):
            # Handle dictionary format
            lat = target_locations.get('lat', 0)
            lon = target_locations.get('lon', 0)
            return weather_data(lat, lon)
        
        elif isinstance(target_locations, (list, tuple)) and len(target_locations) >= 2:
            # Handle list/tuple format
            lat = float(target_locations[0])
            lon = float(target_locations[1])
            return weather_data(lat, lon)
            
        else:
            return "Invalid location format provided. Expected format: 'lat,lon' or dict with lat/lon keys"
            
    except Exception as e:
        return f"Error analyzing weather: {str(e)}"
