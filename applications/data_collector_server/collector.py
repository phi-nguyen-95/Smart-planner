import requests

GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

def get_coordinates(location):
    """
    Convert a location name into latitude and longitude.
    """
    response = requests.get(GEO_URL, params={"name": location, "count": 1, "language": "en", "format": "json"}, timeout=10)
    response.raise_for_status()
    data = response.json()
    results = data.get("results", [])
    if not results:
        raise ValueError(f"Location not found: {location}")
    place = results[0]
    name_parts = [place.get("name"), place.get("admin1"), place.get("country")]
    display_name = ", ".join(part for part in name_parts if part)
    return {"latitude": place["latitude"], "longitude": place["longitude"], "display_name": display_name}

def collect_weather(location):
    """
    Collect current weather information for a location.
    """
    coordinates = get_coordinates(location)
    response = requests.get(
	WEATHER_URL,
        params={"latitude": coordinates["latitude"], "longitude": coordinates["longitude"],
        "current": ("temperature_2m", "relative_humidity_2m", "precipitation", "wind_speed_10m"),
        "timezone": "auto"}, timeout=10)
    response.raise_for_status()
    data = response.json()
    current = data.get("current")
    if not current:
        raise ValueError("Current weather data was not returned.")
    return {
        "location": coordinates["display_name"],
        "latitude": coordinates["latitude"],
        "longitude": coordinates["longitude"],
        "temperature": current["temperature_2m"],
        "humidity": current["relative_humidity_2m"],
        "precipitation": current["precipitation"],
        "wind_speed": current["wind_speed_10m"],
        "observed_at": current["time"],
    }

