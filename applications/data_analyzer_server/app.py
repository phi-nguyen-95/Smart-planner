from flask import Flask, jsonify, request
from applications.data_analyzer_server.analyzer import calculate_activity_score, get_activity_rating
from components.database.repository import get_recent_weather

app = Flask(__name__)

@app.route("/api/analysis/latest")
def analyze_latest_weather():
    records = get_recent_weather(limit=1)
    if not records:
        return jsonify({"error": "No weather records found"}), 404
    record = records[0]
    score = calculate_activity_score(
        temperature=record.temperature,
        precipitation=record.precipitation
        wind_speed=record.wind_speed,
        humidity=record.humidity)
    rating = get_activity_rating(score)
    return jsonify({
        "record_id": record.id,
        "location": record.location,
        "temperature": record.temperature,
        "humidity": record.humidity,
        "precipitation": record.precipitation,
        "wind_speed": record.wind_speed,
        "activity_score": score,
        "activity_rating": rating,
        "observed_at": record.observed_at})

@app.route("/api/analysis/summary")

