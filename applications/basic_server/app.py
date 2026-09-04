from flask import Flask, render_template, request

from applications.data_collector_server.collector import collect_weather
from components.analysis_client import get_latest_analysis, get_trend_analysis
from components.database.repository import save_weather, get_recent_weather

app = Flask(__name__)


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
