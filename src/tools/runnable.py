from langchain_core.tools import tool
from src.tools.fire_data import fire_data
from src.tools.weather_data import weather_data
from src.tools.web_search import go_websearch



@tool
def get_fire_data_tool(lat: float, lon: float) -> str:
    """
    Retrieves recent fire data from NASA FIRMS API for given latitude and longitude.

    Args:
        lat (float): Latitude of the location.
        lon (float): Longitude of the location.

    Returns:
        str: Fire activity data for the region.
    """
    return fire_data(lat, lon)


@tool
def get_weather_data_tool(lat: float, lon: float) -> str:
    """
    Retrieves current or forecasted weather data for given latitude and longitude.

    Args:
        lat (float): Latitude of the location.
        lon (float): Longitude of the location.
a
    Returns:
        str: Weather data for the location.
    """
    return weather_data(lat, lon)


@tool
def go_websearch_tool(location: str) -> str:
    """
    Performs a live web search for the given location and returns top results.

    Args:
        location: The search location.

    Returns:
        str: Web search results in a summarized string format.
    """
    return go_websearch(location)
