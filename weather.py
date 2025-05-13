import os
import json
import requests

API_KEY = os.getenv("WEATHERAPI_KEY")
LOCATION = "San Francisco"
OUTPUT_PATH = "weather.json"

def fetch_weather():
    url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={LOCATION}"
    res = requests.get(url)
    data = res.json()

    print("🌤️ Raw WeatherAPI response:")
    print(json.dumps(data, indent=2))

    if "error" in data:
        print("❌ WeatherAPI Error:", data["error"])
        raise Exception(f"WeatherAPI Error: {data['error']['message']}")

    result = {
        "temp_f": data["current"]["temp_f"],
        "temp_c": data["current"]["temp_c"],
        "condition": data["current"]["condition"]["text"]
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(result, f, indent=2)

if __name__ == "__main__":
    fetch_weather()