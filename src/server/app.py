from flask import Flask, jsonify, render_template
import os
import json
import threading
import time
# from src.executables.executable import executable
from agent.main_agent import PredictFirePlaces


app = Flask(__name__, static_folder="static", template_folder="static/templates")



# def run_every_30_minutes():
#     while True:
#         print("Running scheduled task...")
#         executable()
#         time.sleep(30)  #30s set for testing purpose, change to 30min later

# def start_scheduler():
#     threading.Thread(target=run_every_30_minutes, daemon=True).start()



@app.route("/", methods=["GET"])
def root():
    return jsonify({
        "status_code": 200,
        "message": "PyroScan-AI API v1 - Ready for fire risk predictions. Use `/predictions` to view fire risk dashboard."
    })
    
    
    
@app.route("/api/v1/predictions", methods=["GET"])
def log_predictions():
    load_predictions = os.path.join(os.getcwd(), "src", "db", "report.ndjson")

    if not os.path.exists(load_predictions):
        return jsonify({
            "status_code": 404,
            "message": "report.ndjson does not exist"
        })

    try:
        with open(load_predictions, "r") as f:
            predictions = [json.loads(line) for line in f if line.strip()]

        return jsonify({
            "status_code": 200,
            "message": "Success",
            "data": predictions
        }), 200

    except json.JSONDecodeError:
        return jsonify({
            "status_code": 500,
            "message": "Invalid JSON format in report.ndjson"
        }), 500


@app.route("/predictions", methods=["GET"])
def html_predictions():
    return render_template("predictions.html")


# start_scheduler()