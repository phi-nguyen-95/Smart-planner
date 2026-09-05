import time
from flask import Flask, render_template, request, jsonify
from prometheus_client import CollectorRegistry, Counter


from applications.data_collector_server.collector import collect_weather
from components.analysis_client import get_latest_analysis, get_trend_analysis
from components.database.repository import save_weather, get_recent_weather

app = Flask(__name__)

# Production monitoring metrics

APP_START_TIME = time.time()
METRICS_REGISTRY = CollectorRegistry()
REQUEST_COUNT = Counter("smart_planner_http_requests",
                        "Total number of HTTP requests handled by Smart Planner",
                        registry=METRICS_REGISTRY)
ERROR_COUNT = Counter("smart_planner_http_errors",
                      "Total number of HTTP 5xx responses",
                      registry=METRICS_REGISTRY)
@app.before_request
def record_request():
    REQUEST_COUNT.inc()

@app.after_request
def record_response(response):
    if response.status_code >= 500:
        ERROR_COUNT.inc()
    return response

@app.route("/health")
def health():
    return jsonify({"status": "ok",
                    "service": "smart-planner-basic-server"}), 200

@app.route("/metrics")
def metrics():
    uptime_seconds = max(time.time() - APP_START_TIME, 0.001)
    total_requests = METRICS_REGISTRY.get_sample_value("smart_planner_http_requests_total") or 0
    total_errors = METRICS_REGISTRY.get_sample_value("smart_planner_http_errors_total") or 0
    requests_per_second = total_requests/uptime_seconds
    return jsonify({
        "service": "smart-planner-basic-server",
        "status": "ok",
        "requests_total": int(total_requests),
        "errors_total": int(total_errors),
        "uptime_seconds": round(uptime_seconds,2),
        "request_per_second": round(requests_per_second,4)
    }), 200


@app.route("/",methods=["GET","POST"])
def home():
    weather=None
    activity_score=None
    activity_rating=None
    error=None
    analysis_error=None
    trend_analysis = None

    if request.method == "POST":
        location = request.form.get("location","").strip()
        if not location:
            error = "Please enter a location."
        else:
            try:
                # Fetch data from external Weather API
                weather = collect_weather(location)
                # Save fetched weather data to database
                save_weather(weather)
            except Exception as exc:
                error = f"Unable to collect weather data: {exc}"
 
            if weather is not None:
                try:
                    # Call the separate Data Analyzer RESTV API
                    analysis = get_latest_analysis()
                    activity_score = analysis["activity_score"]
                    activity_rating = analysis["activity_rating"]
                    trend_analysis = get_trend_analysis(weather["location"])
                except Exception as exc:
                    analysis_error = f"Unable to contact Data Analyzer service: {exc}"

    try:
        history = get_recent_weather(limit=10)
    except Exception:
        history=[]

    return render_template("index.html", weather=weather, activity_score=activity_score,
    activity_rating=activity_rating, history=history, error=error, analysis_error=analysis_error,
    trend_analysis=trend_analysis)


if __name__ == "__main__":
    app.run(debug=True)
