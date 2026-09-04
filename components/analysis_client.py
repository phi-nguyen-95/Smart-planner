import os
import requests

ANALYZER_BASE_URL = os.getenv("ANALYZER_BASE_URL", "http://127.0.0.1:5001").rstrip("/")

def get_latest_analysis():
    """
    Request analysis from the Data Analyzer REST service.
    """
    response = requests.get(f"{ANALYZER_BASE_URL}/api/analysis/latest", timeout=5)
    response.raise_for_status()
    return response.json()

def get_trend_analysis(location):
    """
    Request weather trend analysis from the Data Analyzer REST service.
    """
    response = requests.get(f"{ANALYZER_BASE_URL}/api/analysis/trend",
               params={"location": location}, timeout=5)

    response.raise_for_status()
    return response.json()

