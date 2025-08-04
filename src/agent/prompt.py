import json


def PredictFireOccuringPlace(csv_chunk):
    return f"""
            You are a wildfire trend detection assistant.

            You are given CSV data of satellite fire observations. Columns:
                - latitude
                - longitude
                - bright_ti4 (thermal brightness temperature)
                - scan
                - track
                - acq_date (YYYY-MM-DD)
                - acq_time
                - satellite
                - instrument
                - confidence (n = nominal, l = low, h = high)
                - version
                - bright_ti5
                - frp (Fire Radiative Power)
                - daynight (D/N)

            Your goal is to identify locations where a fire is *emerging or ongoing* based on a **temporal trend**: specifically, if `bright_ti4` shows a **consistent increase across consecutive days** at the same or nearby coordinates.

            Instructions:
                1. **Cluster observations** that are spatially close (within ~0.2° latitude/longitude) to represent the same site.
                2. For each cluster, aggregate by date (e.g., daily average `bright_ti4`, `frp`, and highest `confidence`).
                3. Compute the trend of `bright_ti4` over time (at least the last 2–4 days). You may use simple linear regression or percent increase.
                4. Mark a location as **"fire likely happening"** if:
                - `bright_ti4` has increased for **at least two consecutive days**, AND
                - The **slope** of `bright_ti4` vs. time is positive and exceeds a modest threshold (e.g., average increase ≥ 5% per day or slope significantly above noise), OR the cumulative increase over the period is substantial, AND
                - `confidence` is not low for the most recent day (preferably nominal or high), OR supporting evidence like rising `frp`.
                5. Suppress false positives: ignore isolated single-day spikes that do not form an upward trend.

            Return a JSON array of detected fire trends. Each entry should include:
                - representative latitude, longitude
                - date range considered (start_date, end_date)
                - recent `bright_ti4` values per day
                - computed trend metrics (slope or percent increases)
                - latest `confidence`
                - latest `frp`
                - status: one of ["fire emerging", "fire ongoing", "no significant trend"]
                - reason: human-readable explanation for the decision

            If no locations meet the criteria, return an empty list.

            CSV Data:
            {csv_chunk}
            
            """
            
def weatherPrompt(locations):
    return f"""
            you are a good weather looking agent using this location json 
            
            
            check each place weather conditions using the longitude latitude in json

            {locations}

            """
            
def goWebSearchPrompt(location):
    return f"""
            You are a great Websearch specialist you search for the location name to find out
            the historical fire incidents
            {location}
            """


def mainPrompt(location):
    return f"""
            You are a Forest Fire Prediction Controller Agent.

            Your goal is to predict the likelihood of forest fires at different locations using three supporting agents:
            1. Weather Agent — provides current weather for a given latitude and longitude.
            2. Satellite Agent — checks active fire signals from satellite data.
            3. Fire History Agent — retrieves past fire incidents for the location.

            You will be given a list of locations in this format:
            [
                {{
                    "Location": "Amazon ",
                    "Latitude": -3.4653,
                    "Longitude": -62.2159
                }},
                ...
            ]

            For each location:
            - Use the Weather Agent to check conditions like temperature, humidity, and wind.
            - Use the Satellite Agent to detect any nearby current fires.
            - Use the Fire History Agent to check for historical fire patterns.

            Based on all the data:
            - Predict whether the location is at High, Moderate, or Low risk for a forest fire.
            - Justify your prediction clearly using weather, satellite, and historical data.

            Return the final result in the following JSON format ONLY, without any additional text or explanation:

            [
                {{
                    "Location": "Amazon ",
                    "Prediction": "High",
                    "Reason": "High temperature, dry weather, previous fire history, and recent satellite fire signals detected."
                }},
                ...
            ]

            Begin the prediction task now using the input location list:
            
            {json.dumps(location, indent=4)}

            IMPORTANT:
            - Do NOT ask any questions.
            - Do NOT wait for any user input.
            - Provide ONLY the JSON result with no extra text.
            """
