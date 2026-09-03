from flask import Flask, render_template, request

from applications.data_collector_server.collector import collect_weather
from applications.data_analyzer_server.analyzer import calculate_activity_score, get_activity_rating
from components.database.repository import save_weather, get_recent_weather

app = Flask(__name__)


@app.route("/",methods=["GET","POST"])
def home():
    weather=None
    activity_score=None
    activity_rating=None
    error=None

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
                # Analyze collected weather
                activity_score = calculate_activity_score(temperature=weather["temperature"],
                precipitation=weather["precipitation"], wind_speed=weather["wind_speed"],
                humidity=weather["humidity"])
                activity_rating = get_activity_rating(activity_score)
            except Exception as exc:
                error = f"Unable to collect weather data: {exc}"
    try:
        history = get_recent_weather(limit=10)
    except Exception:
        history=[]

    return render_template("index.html", weather=weather, activity_score=activity_score,
    activity_rating=activity_rating, history=history, error=error)


if __name__ == "__main__":
    app.run(debug=True)
