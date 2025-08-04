#  PyroScan AI - Agentic AI For Forest Fire Prediction 

PyroScan AI is an intelligent agentic AI system designed to predict and monitor forest fires using real-time satellite data from NASA FIRMS API and advanced machine learning techniques. The system provides early warning capabilities and comprehensive fire risk assessment for critical forest regions worldwide.

##  Features

- **Real-time Fire Detection**: Fetches live fire data from NASA FIRMS satellite API
- **Multi-Region Monitoring**: Tracks fire incidents in 10 critical forest regions globally
- **Intelligent Filtering**: Filters fire data based on proximity to high-risk areas
- **Agentic Decision Making**: AI-powered analysis and prediction capabilities
- **Geographic Analysis**: Location-based fire risk assessment


## Target Monitoring Regions

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

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/DeveloperAromal/PyroScan-AI.git
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

PyroScan-AI
├─ .dockerignore
├─ Dockerfile
├─ main.py
├─ pyroscan-ai.toml
├─ README.md
├─ requirements.txt
├─ run.sh
├─ src
│  ├─ agent
│  │  ├─ fire_spot_agent.py
│  │  ├─ main_agent.py
│  │  ├─ prompt.py
│  │  ├─ risk_score_agent.py
│  │  ├─ weather_agent.py
│  │  └─ web_search_agent.py
│  ├─ data
│  │  └─ danger-zone.csv
│  ├─ db
│  ├─ server
│  │  ├─ app.py
│  │  └─ static
│  │     └─ templates
│  │        └─ predictions.html
│  ├─ tools
│  │  ├─ fire_data.py
│  │  ├─ runnable.py
│  │  ├─ weather_data.py
│  │  └─ web_search.py
│  └─ utils
│     ├─ get_cordinates.py
│     └─ unique_id.py
└─ workflow.mmd

```

## Usage

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

### Running on Docker

```bash
docker build -t pyroscan-ai .

docker run -p 8483:8483 --env-file .env pyroscan-ai
```



## Data Sources

- **NASA FIRMS API**: Real-time satellite fire detection data
- **VIIRS Satellite**: Visible Infrared Imaging Radiometer Suite
- **NRT Data**: Near Real-Time fire detection

## AI Components

- **Decision Maker**: AI agent for fire risk assessment
- **Heat Map Classifier**: Machine learning for fire pattern analysis
- **Prompt Engineering**: Optimized prompts for AI analysis

## Safety Features

- Real-time monitoring of critical forest regions
- Early warning system for fire outbreaks
- Geographic proximity analysis
- Risk assessment algorithms



## Flowchart

![Diagram](workflow.mmd)

## Disclaimer

PyroScan AI is designed for research and monitoring purposes. Always follow local emergency protocols and contact appropriate authorities in case of actual fire emergencies.


**Drop a star on GitHub if you like it!** 
```