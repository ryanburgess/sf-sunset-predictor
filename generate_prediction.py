import requests
from datetime import datetime, timedelta
import pytz
import json
import os
import subprocess
from astral import LocationInfo
from astral.moon import moonrise, moonset
from datetime import date

# Only load .env file if it exists (for local development)
if os.path.exists(".env"):
    from dotenv import load_dotenv
    load_dotenv()

def get_moon_info():
    city = LocationInfo("San Francisco", "USA", "America/Los_Angeles", 37.7749, -122.4194)
    today = date.today()
    tz = pytz.timezone(city.timezone)

    try:
        rise = moonrise(city.observer, date=today)
        set_ = moonset(city.observer, date=today)

        return {
            "moonrise": rise.astimezone(tz).strftime("%-I:%M %p") if rise else None,
            "moonset": set_.astimezone(tz).strftime("%-I:%M %p") if set_ else None
        }
    except Exception as e:
        print(f"⚠️ Error computing moon info: {e}")
        return {
            "moonrise": None,
            "moonset": None
        }

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
def get_prediction_scores(moon_data):
    API_KEY = os.environ.get("VISUAL_CROSSING_API_KEY")
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
                "moonrise": moon_data.get("moonrise"),
                "moonset": moon_data.get("moonset")
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
    API_KEY = os.environ.get("METEOSOURCE_API_KEY")
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

def analyze_twilight_conditions(sun_times, fog_forecast):
    from_zone = pytz.timezone("America/Los_Angeles")

    def parse_time_to_dt(time_str):
        now = datetime.now()
        today = now.date()
        parsed = datetime.strptime(time_str, "%I:%M %p")
        combined = datetime.combine(today, parsed.time())
        return from_zone.localize(combined)

    def parse_forecast_time(forecast_time_str):
        return datetime.fromisoformat(forecast_time_str).astimezone(from_zone)

    # Build twilight windows with real datetime objects
    twilight_windows = [
        {
            "label": "Astronomical Twilight",
            "start": parse_time_to_dt(sun_times["astronomical_twilight_begin"]),
            "end": parse_time_to_dt(sun_times["nautical_twilight_begin"])
        },
        {
            "label": "Nautical Twilight",
            "start": parse_time_to_dt(sun_times["nautical_twilight_begin"]),
            "end": parse_time_to_dt(sun_times["civil_twilight_begin"])
        },
        {
            "label": "Civil Twilight",
            "start": parse_time_to_dt(sun_times["civil_twilight_begin"]),
            "end": parse_time_to_dt(sun_times["sunrise"])
        },
        {
            "label": "Golden Hour",
            "start": parse_time_to_dt(sun_times["sunrise"]),
            "end": parse_time_to_dt(sun_times["sunrise"]) + timedelta(hours=1)
        }
    ]

    recommended = None
    for window in twilight_windows:
        matching_fog = [
            f for f in fog_forecast
            if "fog_score" in f and f["fog_score"] is not None and
               window["start"] <= parse_forecast_time(f["time"]) <= window["end"]
        ]
        if matching_fog:
            avg_fog = sum(f["fog_score"] for f in matching_fog) / len(matching_fog)
            window["avg_fog_score"] = round(avg_fog, 2)
            if recommended is None or avg_fog < recommended["fog_score"]:
                recommended = {
                    "time": window["start"].strftime("%-I:%M %p"),
                    "phase": window["label"],
                    "fog_score": round(avg_fog, 2)
                }
        else:
            window["avg_fog_score"] = None

        # Format for JSON
        window["start"] = window["start"].strftime("%-I:%M %p")
        window["end"] = window["end"].strftime("%-I:%M %p")

    if recommended and recommended["fog_score"] <= 5:
        summary = (
            f"Best time to shoot: {recommended['time']} — "
            f"low fog ({recommended['fog_score']}) during {recommended['phase']}."
        )
    else:
        summary = "No optimal low-fog window during twilight today. Consider shooting at sunset or when fog clears."

    return twilight_windows, recommended, summary

# -----------------------------
# 📝 Step 4: Write predictions.json
# -----------------------------
def create_prediction_json():
    sun_times = get_sunrise_sunset_times()
    moon_data = get_moon_info()
    scores = get_prediction_scores(moon_data)
    fog_forecast = get_fog_forecast()
    twilight_phases, recommended_window, summary = analyze_twilight_conditions(sun_times, fog_forecast)
    updated_at = datetime.now(pytz.utc).isoformat()

    prediction = {
        **sun_times,
        "sunrise_score": scores["sunrise_score"],
        "sunset_score": scores["sunset_score"],
        "moon_phase": scores["moon_phase"],
        "fog_forecast": fog_forecast,
        "twilight_phases": twilight_phases,
        "recommended_shoot_time": recommended_window,
        "summary_text": summary,
        "updated_at": updated_at
    }

    with open("predictions.json", "w") as f:
        json.dump(prediction, f, indent=2)

    print("✅ predictions.json created!")

# -----------------------------
# 🏁 Run Everything
# -----------------------------
if __name__ == "__main__":
    create_prediction_json()