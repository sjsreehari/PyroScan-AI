from src.tools.fire_data import get_fire_data_by_location
from src.tools.heat_map_classifer import process_all_heatmaps

def executable():
    get_fire_data_by_location() # Added heatmap api things 
    # process_all_heatmaps() # Added heatmap api things