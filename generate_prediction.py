import requests
from datetime import datetime
import pytz
import json
import subprocess

# Step 1: Get sunrise/sunset times for SF in UTC and convert to PST/PDT
def get_sunrise_sunset_times():
    url = "https://api.sunrise-sunset.org/json?lat=37.7749&lng=-122.4194&formatted=0"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        pacific = pytz.timezone("America/Los_Angeles")

        # No need to localize if the datetime string already has a timezone
        sunrise_utc = datetime.fromisoformat(data['results']['sunrise'])
        sunset_utc = datetime.fromisoformat(data['results']['sunset'])

        sunrise_local = sunrise_utc.astimezone(pacific).strftime("%-I:%M %p")
        sunset_local = sunset_utc.astimezone(pacific).strftime("%-I:%M %p")

        return sunrise_local, sunset_local

    except Exception as e:
        print(f"⚠️ Error fetching sunrise/sunset times: {e}")
        return "6:00 AM", "8:00 PM"

# Step 2: Use Visual Crossing Weather API to get forecast + prediction scores
def get_prediction_scores():
    API_KEY = "H2EWPGQHW8R95XYNWGWGPT8SL"  # Replace with your API key
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/san%20francisco/today?unitGroup=us&include=hours&key={API_KEY}&contentType=json"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        hours = data["days"][0]["hours"]

        # Pull actual forecasted sunrise/sunset hour from the same data source
        sunrise_time = data["days"][0]["sunrise"]  # e.g. "06:48:20"
        sunset_time = data["days"][0]["sunset"]    # e.g. "19:36:48"
        sunrise_hour = int(sunrise_time.split(":")[0])
        sunset_hour = int(sunset_time.split(":")[0])

        def find_hour_score(hour_data):
            cloud = hour_data.get("cloudcover", 100)
            vis = hour_data.get("visibility", 0)
            cloud_score = max(0, 10 - abs(cloud - 45) / 5)
            vis_score = min(vis / 10, 1.0) * 10
            return int((cloud_score * 0.7 + vis_score * 0.3))

        sunrise_score = 0
        sunset_score = 0

        for hour in hours:
            hour_str = hour["datetime"]  # e.g., "06:00:00"
            hour_val = int(hour_str.split(":")[0])
            if hour_val == sunrise_hour:
                sunrise_score = find_hour_score(hour)
            elif hour_val == sunset_hour:
                sunset_score = find_hour_score(hour)

        return {
            "sunrise_score": sunrise_score,
            "sunset_score": sunset_score
        }

    except Exception as e:
        print(f"⚠️ Error fetching weather data: {e}")
        return {
            "sunrise_score": 5,
            "sunset_score": 5
        }

# Step 3: Write final output to JSON
def create_prediction_json():
    sunrise, sunset = get_sunrise_sunset_times()
    scores = get_prediction_scores()
    updated_at = datetime.now(pytz.utc).isoformat()

    prediction = {
        "sunrise": sunrise,
        "sunset": sunset,
        "sunrise_score": scores["sunrise_score"],
        "sunset_score": scores["sunset_score"],
        "updated_at": updated_at
    }

    with open("predictions.json", "w") as f:
        json.dump(prediction, f, indent=2)

    print("✅ predictions.json created!")

# Run it
if __name__ == "__main__":
    create_prediction_json()


def git_commit_and_push():
    try:
        subprocess.run(["git", "add", "predictions.json"], check=True)
        subprocess.run(["git", "commit", "-m", "Update predictions"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("✅ Git push completed.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Git error: {e}")

# Run all
if __name__ == "__main__":
    create_prediction_json()
    git_commit_and_push()