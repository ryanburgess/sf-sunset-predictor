import requests
from datetime import datetime
import pytz
import json
import subprocess
import config

# -----------------------------
# 🌅 Step 1: Sunrise/Sunset + Twilight
# -----------------------------
def get_sunrise_sunset_times():
    url = "https://api.sunrise-sunset.org/json?lat=37.7749&lng=-122.4194&formatted=0"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        results = data['results']

        pacific = pytz.timezone("America/Los_Angeles")

        def to_local(time_str):
            utc_dt = datetime.fromisoformat(time_str)
            return utc_dt.astimezone(pacific).strftime("%-I:%M %p")

        return {
            "sunrise": to_local(results['sunrise']),
            "sunset": to_local(results['sunset']),
            "solar_noon": to_local(results['solar_noon']),
            "civil_twilight_begin": to_local(results['civil_twilight_begin']),
            "civil_twilight_end": to_local(results['civil_twilight_end']),
            "nautical_twilight_begin": to_local(results['nautical_twilight_begin']),
            "nautical_twilight_end": to_local(results['nautical_twilight_end']),
            "astronomical_twilight_begin": to_local(results['astronomical_twilight_begin']),
            "astronomical_twilight_end": to_local(results['astronomical_twilight_end']),
            "day_length": results['day_length']
        }

    except Exception as e:
        print(f"⚠️ Error fetching sunrise/sunset times: {e}")
        return {
            "sunrise": "6:00 AM",
            "sunset": "8:00 PM",
            "solar_noon": "12:00 PM",
            "civil_twilight_begin": "5:30 AM",
            "civil_twilight_end": "8:30 PM",
            "nautical_twilight_begin": "5:00 AM",
            "nautical_twilight_end": "9:00 PM",
            "astronomical_twilight_begin": "4:30 AM",
            "astronomical_twilight_end": "9:30 PM",
            "day_length": "12:00:00"
        }

# -----------------------------
# 🌤 Step 2: Prediction Scores + Moon Phase
# -----------------------------
def get_prediction_scores():
    API_KEY = config.VISUAL_CROSSING_API_KEY
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/san%20francisco/today?unitGroup=us&include=days,hours,astronomy&key={API_KEY}&contentType=json"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        hours = data["days"][0]["hours"]
        sunrise_time = data["days"][0]["sunrise"]
        sunset_time = data["days"][0]["sunset"]
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
            hour_str = hour["datetime"]
            hour_val = int(hour_str.split(":")[0])
            if hour_val == sunrise_hour:
                sunrise_score = find_hour_score(hour)
            elif hour_val == sunset_hour:
                sunset_score = find_hour_score(hour)

        moon_phase_value = data["days"][0].get("moonphase")
        moonrise = data["days"][0].get("moonrise")
        moonset = data["days"][0].get("moonset")
        moon_label = get_moon_phase_label(moon_phase_value)

        return {
            "sunrise_score": sunrise_score,
            "sunset_score": sunset_score,
            "moon_phase": {
                "value": moon_phase_value,
                "label": moon_label,
                "moonrise": moonrise,
                "moonset": moonset
            }
        }

    except Exception as e:
        print(f"⚠️ Error fetching weather data: {e}")
        return {
            "sunrise_score": 5,
            "sunset_score": 5,
            "moon_phase": {
                "value": None,
                "label": "Unknown",
                "moonrise": None,
                "moonset": None
            }
        }

# -----------------------------
# 🌕 Helper: Moon Phase Label
# -----------------------------
def get_moon_phase_label(value):
    if value is None:
        return "Unknown"
    if value == 0 or value == 1:
        return "New Moon" if value == 0 else "Full Moon"
    elif 0 < value < 0.25:
        return "Waxing Crescent"
    elif value == 0.25:
        return "First Quarter"
    elif 0.25 < value < 0.5:
        return "Waxing Gibbous"
    elif value == 0.5:
        return "Full Moon"
    elif 0.5 < value < 0.75:
        return "Waning Gibbous"
    elif value == 0.75:
        return "Last Quarter"
    else:
        return "Waning Crescent"

# -----------------------------
# 🌫 Step 3: Fog Forecast (Meteosource)
# -----------------------------
def get_fog_forecast():
    API_KEY = config.METEOSOURCE_API_KEY
    url = f"https://www.meteosource.com/api/v1/free/point?place_id=san-francisco&sections=hourly&timezone=auto&language=en&units=us&key={API_KEY}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        fog_data = []
        for hour in data["hourly"]["data"][:12]:
            time = hour.get("date")
            visibility = hour.get("visibility")
            cloud_cover_data = hour.get("cloud_cover")

            if isinstance(cloud_cover_data, dict):
                cloud_total = cloud_cover_data.get("total")
            else:
                cloud_total = cloud_cover_data

            fog_score = calculate_fog_score(visibility, cloud_total)

            fog_data.append({
                "time": time,
                "visibility": visibility if visibility is not None else "unknown",
                "cloud_cover": {
                    "total": cloud_total
                },
                "fog_score": fog_score
            })

        return fog_data

    except Exception as e:
        print(f"⚠️ Error fetching fog forecast: {e}")
        return []

def calculate_fog_score(visibility, cloud_cover):
    if cloud_cover is None:
        return None
    if visibility is None:
        return round(min(cloud_cover / 10, 10), 1)
    score = 10 - min(visibility, 10) + (cloud_cover / 20)
    return round(min(max(score, 0), 10), 1)

# -----------------------------
# 📝 Step 4: Write predictions.json
# -----------------------------
def create_prediction_json():
    sun_times = get_sunrise_sunset_times()
    scores = get_prediction_scores()
    fog_forecast = get_fog_forecast()
    updated_at = datetime.now(pytz.utc).isoformat()

    prediction = {
        **sun_times,
        "sunrise_score": scores["sunrise_score"],
        "sunset_score": scores["sunset_score"],
        "moon_phase": scores["moon_phase"],
        "fog_forecast": fog_forecast,
        "updated_at": updated_at
    }

    with open("predictions.json", "w") as f:
        json.dump(prediction, f, indent=2)

    print("✅ predictions.json created!")

# -----------------------------
# 🚀 Git Auto-commit
# -----------------------------
def git_commit_and_push():
    try:
        subprocess.run(["git", "add", "predictions.json"], check=True)
        subprocess.run(["git", "commit", "-m", "Update predictions"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("✅ Git push completed.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Git error: {e}")

# -----------------------------
# 🏁 Run Everything
# -----------------------------
if __name__ == "__main__":
    create_prediction_json()
    git_commit_and_push()