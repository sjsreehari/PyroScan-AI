import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
HEATMAP_API_KEY = os.getenv("HEATMAP_API_KEY", "")
HEATMAP_API_URL = os.getenv("HEATMAP_API_URL", "https://heatmapapi.com/heatmapapiservices/api/createHeatmap")

# File Paths
FIREMAP_DIR = BASE_DIR / "src" / "db" / "firemap-storage"
COORDINATES_DIR = BASE_DIR / "src" / "db" / "coordinates_location"
DATA_DIR = BASE_DIR / "src" / "data"
ALERT_FILE = COORDINATES_DIR / "alert.ndjson"
DANGER_ZONE_CSV = DATA_DIR / "danger-zone.csv"

# Heatmap Configuration
LAT_RANGE = 0.1
LON_RANGE = 0.1
NUM_POINTS = 50
RADIUS_MILES = 1
WIDTH, HEIGHT = 400, 300

# Application Settings
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Ensure directories exist
FIREMAP_DIR.mkdir(parents=True, exist_ok=True)
COORDINATES_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True) 