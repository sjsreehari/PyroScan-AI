#  PyroScan AI - Agentic AI For Forest Fire Prediction 

PyroScan AI is an intelligent agentic AI system designed to predict and monitor forest fires using real-time satellite data from NASA FIRMS API and advanced machine learning techniques. The system provides early warning capabilities and comprehensive fire risk assessment for critical forest regions worldwide.

##  Features

- **Real-time Fire Detection**: Fetches live fire data from NASA FIRMS satellite API
- **Multi-Region Monitoring**: Tracks fire incidents in 10 critical forest regions globally
- **Intelligent Filtering**: Filters fire data based on proximity to high-risk areas
- **Agentic Decision Making**: AI-powered analysis and prediction capabilities
- **Geographic Analysis**: Location-based fire risk assessment


## 🎯 Target Monitoring Regions

The system monitors fire incidents in these critical forest regions:

- **Amazon Rainforest** (Brazil)
- **California Wildlands** (USA)
- **British Columbia** (Canada)
- **Siberia Forests** (Russia)
- **Athens Outskirts** (Greece)
- **Canberra Region** (Australia)
- **Alberta Forests** (Canada)
- **Western Cape** (South Africa)
- **Mato Grosso** (Brazil)
- **Los Angeles National Forest** (USA)

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd PyroScan-AI
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

##  API Keys Setup

PyroScan AI requires API keys for external services. Create a `.env` file in the project root with the following keys:

### Required API Keys

1. **NASA FIRMS API Key**
   - Get your API key from: https://firms.modaps.eosdis.nasa.gov/api/
   - Add to `.env` file:
   ```
   NASA_FIRM_API_KEY=your_nasa_api_key_here
   ```

2. **OpenRouter API Key**
   - Get your API key from: https://openrouter.ai/settings/keys
   - Add to `.env` file:
   ```
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   ```

### Example `.env` file:
```
NASA_FIRM_API_KEY=9b****************04c6ee
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

## Project Structure

```
PyroScan-AI/
├── main.py                   # Main application entry point
├── requirements.txt          # Python dependencies
├── src/
│   ├── agent/               # AI agent components
│   │   ├── decision_maker.py
│   │   └── prompt.py
│   ├── data/                # Data files
│   │   └── danger-zone.csv
│   ├── db/                  # Database and storage
│   │   ├── fire_data.csv
│   │   ├── fire_data_by_danger_zone.csv
│   │   ├── fire_data_location.csv
│   │   └── firemap-storage/
│   ├── executables/         # Executable scripts
│   │   └── executable.py
│   ├── server/              # Web server components
│   │   ├── app.py
│   │   └── fire_map.py
│   ├── tools/               # Core tools and utilities
│   │   ├── fire_data.py     # Fire data fetching and processing
│   └── utils/               # Utility functions
│       ├── get_coordinates.py
│       └── unique_id.py
└── venv/                    # Virtual environment
```

## 🛠️ Usage

### Running the Fire Data Tool

```bash
python src/tools/fire_data.py
```

This will:
- Fetch real-time fire data from NASA FIRMS API
- Filter data for monitored regions
- Save filtered data to `src/db/filtered_fire_data.csv`

### Running the Main Application

```bash
python main.py
```

### Running the Web Server

```bash
python src/server/app.py
```

## 📊 Data Sources

- **NASA FIRMS API**: Real-time satellite fire detection data
- **VIIRS Satellite**: Visible Infrared Imaging Radiometer Suite
- **NRT Data**: Near Real-Time fire detection

## 🤖 AI Components

- **Decision Maker**: AI agent for fire risk assessment
- **Heat Map Classifier**: Machine learning for fire pattern analysis
- **Prompt Engineering**: Optimized prompts for AI analysis

## 🚨 Safety Features

- Real-time monitoring of critical forest regions
- Early warning system for fire outbreaks
- Geographic proximity analysis
- Risk assessment algorithms


## ⚠️ Disclaimer

PyroScan AI is designed for research and monitoring purposes. Always follow local emergency protocols and contact appropriate authorities in case of actual fire emergencies.


**Drop a star on GitHub if you like it!** 