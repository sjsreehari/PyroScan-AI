from flask import Flask, jsonify
import os
import json

app = Flask(__name__)





@app.route("/", methods=["GET"])
def root():
    return jsonify({
        "status_code": 200,
        "message": "PyroScan-AI API v1 - Ready for fire risk predictions. Use `/api/v1/predictions` to get started."
    })


@app.route("/api/v1/predictions", methods=["GET"])
def log_predictions():
    load_predictions = os.path.join(os.getcwd(), "src", "db", "report.json")
    
    if not os.path.exists(load_predictions):
        return jsonify({
            "status_code":404,
            "message": "report.json does not exist"
        })
    
    try:
    
        with open(load_predictions, "r") as f:
            predictions = json.load(f)
            return jsonify({
                            "status_code": 200,
                            "message": "Success",
                            "data": predictions
                            }), 200
        
    except json.JSONDecodeError:
        
        return jsonify({
            "status_code": 500,
            "message": "Invalid JSON format in report.json"
        }), 500


