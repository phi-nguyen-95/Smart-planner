from flask import Flask, jsonify, request
from applications.data_analyzer_server.analyzer import calculate_activity_score, get_activity_rating
from components.database.repository import get_recent_weather, get_recent_weather_by_location
from applications.data_analyzer_server.analyzer import analyze_weather_trend 

app = Flask(__name__)

@app.route("/api/analysis/latest")
def analyze_latest_weather():
    records = get_recent_weather(limit=1)
    if not records:
        return jsonify({"error": "No weather records found"}), 404
    record = records[0]
    score = calculate_activity_score(
        temperature=record.temperature,
        precipitation=record.precipitation,
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
def analysis_summary():
    limit = request.args.get("limit", default=10, type=int)
    records = get_recent_weather(limit=limit)
    if not records:
        return jsonify({"error": "No weather records found"}), 404
    temperatures = [record.temperature for record in records]
    humidities = [record.humidity for record in records]
    activity_scores = []
    for record in records:
        score = calculate_activity_score(temperature=record.temperature,
        precipitation=record.precipitation, wind_speed=record.wind_speed,
        humidity=record.humidity)
        activity_scores.append(score)

    average_temperature = (sum(temperatures)/len(temperatures))
    average_humidity = (sum(humidities)/len(humidities))
    average_activity_score = (sum(activity_scores)/len(activity_scores))
    return jsonify({
        "record_analyzed": len(records),
        "average_temperature": round(average_temperature, 2),
        "average_humidity": round(average_humidity, 2),
        "average_activity_score": round(average_activity_score, 2),
        "overall_rating": get_activity_rating(average_activity_score)})

@app.route("/api/analysis/trend")
def weather_trend():
    location = request.args.get("location", "").strip()
    if not location:
        return jsonify({"error": "Location parameter is required"}), 400
    records = get_recent_weather_by_location(location=location, limit=2)
    if len(records) < 2:
        return jsonify({"status": "insufficient_data", "location": location,
        "message": "At least two weather records are required"})
    current = records[0]
    previous = records[1]
    trend = analyze_weather_trend(current=current, previous=previous)
    return jsonify({"status": "ok", "location": location, **trend})


if __name__ == "__main__":
    app.run(port=5001, debug=True)

