"""
This is the agent that gathers past incidents happened on that place using web search
"""

from src.tools.web_search import go_websearch
import os

def analyse_historical_data(target_locations_name):
    print("Searching the place.....")
    
    try:
        # Handle different input formats
        def safe_search(query):
            result = go_websearch(query)
            if not result or result.strip() == "":
                return f"No historical fire incidents found for '{query}'."
            return result

        if isinstance(target_locations_name, str):
            return safe_search(target_locations_name)
        elif isinstance(target_locations_name, dict):
            # Extract location name from dictionary
            location_name = target_locations_name.get('name', '')
            if location_name:
                return safe_search(location_name)
            else:
                return "No location name found in provided data"
        else:
            return "Invalid location format provided. Expected string or dict with 'name' key"
    except Exception as e:
        return f"Error searching historical data: {str(e)}"