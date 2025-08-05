"""
This is the agent that gets weather data
"""

from src.tools.weather_data import weather_data
import re


def analyse_the_weather(target_locations):
    print("weather place analysis started.....")
    
    
    try:
        if isinstance(target_locations, str):
            if 'lat=' in target_locations and 'lon=' in target_locations:
                
                lat_match = re.search(r'lat=([\d.\-]+)', target_locations)
                lon_match = re.search(r'lon=([\d.\-]+)', target_locations)
                
                
                if lat_match and lon_match:
                    lat = float(lat_match.group(1))
                    lon = float(lon_match.group(1))
                    return weather_data(lat, lon)
                
                
            coords = target_locations.strip().split(',')
            
            if len(coords) == 2:
                lat = float(coords[0].strip())
                lon = float(coords[1].strip())
                return weather_data(lat, lon)
            
            
        elif isinstance(target_locations, dict):
            lat = float(target_locations.get('lat', 0))
            lon = float(target_locations.get('lon', 0))
            return weather_data(lat, lon)
        
        
        elif isinstance(target_locations, (list, tuple)) and len(target_locations) >= 2:
            lat = float(target_locations[0])
            lon = float(target_locations[1])
            return weather_data(lat, lon)
        
        
        else:
            return "Invalid location format provided. Expected format: 'lat,lon', 'lat=<latitude>, lon=<longitude>', or dict/list with lat/lon."
        
        
    except Exception as e:
        return f"Error analyzing weather: {str(e)}"