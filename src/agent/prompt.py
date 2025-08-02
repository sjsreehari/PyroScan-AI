


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