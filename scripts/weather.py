import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WEATHERAPI_KEY")
LOCATION = "San Francisco"
OUTPUT_PATH = "weather.json"

def fetch_weather():
    url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={LOCATION}"
    res = requests.get(url)
    data = res.json()

    result = {
        "temp_f": data["current"]["temp_f"],
        "condition": data["current"]["condition"]["text"]
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(result, f, indent=2)

if __name__ == "__main__":
    fetch_weather()