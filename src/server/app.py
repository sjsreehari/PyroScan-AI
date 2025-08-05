from flask import Flask, jsonify, render_template
from flask_cors import CORS
import os
import json


app = Flask(__name__, static_folder="static", template_folder="static/templates")


CORS(app)



@app.route("/", methods=["GET"])
def root():
    
    return jsonify({
        "status_code": 200,
        "message": "PyroScan-AI API v1 - Ready for fire risk predictions. Use `/api/v1/predictions` to view fire risk data."
    })


@app.route("/api/v1/predictions", methods=["GET"])
def log_predictions():
    
    load_predictions = os.path.join(os.getcwd(), "src", "db", "processed", "prediction.json")



    if not os.path.exists(load_predictions):
        return jsonify({
            "status_code": 404,
            "message": "predictions.json does not exist"
        }), 404



    try:
        with open(load_predictions, "r") as f:
            predictions = json.load(f) 

        return jsonify(predictions), 200  


    except json.JSONDecodeError:
        return jsonify({
            "status_code": 500,
            "message": "Invalid JSON format in predictions.json"
        }), 500

