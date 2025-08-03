from flask import Flask, jsonify, render_template
import os
import json

app = Flask(__name__, static_folder="static", template_folder="static/templates")


@app.route("/", methods=["GET"])
def root():
    return jsonify({
        "status_code": 200,
        "message": "PyroScan-AI API v1 - Ready for fire risk predictions. Use `/predictions` to view fire risk dashboard."
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
        
        
        
@app.route("/predictions", methods=["GET"])
def html_predictions():
    file_path = os.path.join(os.getcwd(), "src", "db", "report.json")
    
    if not os.path.exists(file_path):
        return "report.json not found", 404

    try:
        with open(file_path, "r") as f:
            predictions = json.load(f)
        
        if not predictions:
            return "No data found in report.json", 404
            
        return render_template("predictions.html", data=predictions)
    
    except json.JSONDecodeError:
        return "Invalid JSON format in report.json", 500

