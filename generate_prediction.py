import requests
from datetime import datetime, timedelta, date
import pytz
import json
import os
from astral import LocationInfo
from astral.sun import sun
from astral.moon import moonrise, moonset, phase as moon_phase_value
from urllib.parse import quote


# Only load .env file if present
if os.path.exists(".env"):
    from dotenv import load_dotenv
    load_dotenv()

VISUAL_CROSSING_API_KEY = os.environ.get("VISUAL_CROSSING_API_KEY")
METEOSOURCE_API_KEY = os.environ.get("METEOSOURCE_API_KEY")

# List of cities with coordinates and timezone
cities = [
    {
        "slug": "san-francisco",
        "name": "San Francisco",
        "timezone": "America/Los_Angeles",
        "observer": LocationInfo("San Francisco", "USA", "America/Los_Angeles", 37.7749, -122.4194).observer
    },
    {
        "slug": "los-angeles",
        "name": "Los Angeles",
        "timezone": "America/Los_Angeles",
        "observer": LocationInfo("Los Angeles", "USA", "America/Los_Angeles", 34.0522, -118.2437).observer
    },
    {
        "slug": "san-diego",
        "name": "San Diego",
        "timezone": "America/Los_Angeles",
        "observer": LocationInfo("San Diego", "USA", "America/Los_Angeles", 32.7157, -117.1611).observer
    },
    {
        "slug": "lake-tahoe",
        "name": "Lake Tahoe",
        "timezone": "America/Los_Angeles",
        "observer": LocationInfo("Lake Tahoe", "USA", "America/Los_Angeles", 39.0968, -120.0324).observer
    },
    {
        "slug": "truckee",
        "name": "Truckee",
        "timezone": "America/Los_Angeles",
        "observer": LocationInfo("Truckee", "USA", "America/Los_Angeles", 39.327962, -120.183253).observer
    },
    {
        "slug": "tokyo",
        "name": "Tokyo",
        "timezone": "Asia/Tokyo",
        "observer": LocationInfo("Tokyo", "Japan", "Asia/Tokyo", 35.6895, 139.6917).observer
    }
]

def format_time(dt, tz):
    if dt is None:
        return None
    return dt.astimezone(tz).strftime("%-I:%M %p")

def get_moon_info(observer, tz):
    today = date.today()
    try:
        rise = moonrise(observer, date=today)
        set_ = moonset(observer, date=today)
        return {
            "moonrise": format_time(rise, tz) if rise else None,
            "moonset": format_time(set_, tz) if set_ else None
        }
    except Exception as e:
        print(f"⚠️ Error computing moon info: {e}")
        return {"moonrise": None, "moonset": None}

def get_city_data(city):
    today = date.today()
    tz = pytz.timezone(city["timezone"])
    observer = city["observer"]

    loc = LocationInfo(city["name"], "USA", city["timezone"], observer.latitude, observer.longitude)

    s = sun(observer, date=today, tzinfo=tz)

    loc.depression = "civil"
    s_civil = sun(observer, date=today, tzinfo=tz)

    loc.depression = "nautical"
    s_nautical = sun(observer, date=today, tzinfo=tz)

    loc.depression = "astronomical"
    s_astro = sun(observer, date=today, tzinfo=tz)

    moon_times = get_moon_info(observer, tz)
    scores = get_prediction_scores(city["name"], moon_times)
    fog = get_fog_forecast(city["slug"])
    twilight, best_time, summary = analyze_twilight_conditions(s_civil, fog)

    return city["slug"], {
        "sunrise": format_time(s["sunrise"], tz),
        "sunset": format_time(s["sunset"], tz),
        "solar_noon": format_time(s["noon"], tz),
        "civil_twilight_begin": format_time(s_civil["dawn"], tz),
        "civil_twilight_end": format_time(s_civil["dusk"], tz),
        "nautical_twilight_begin": format_time(s_nautical["dawn"], tz),
        "nautical_twilight_end": format_time(s_nautical["dusk"], tz),
        "astronomical_twilight_begin": format_time(s_astro["dawn"], tz),
        "astronomical_twilight_end": format_time(s_astro["dusk"], tz),
        "day_length": int((s["sunset"] - s["sunrise"]).total_seconds()),
        "sunrise_score": scores["sunrise_score"],
        "sunset_score": scores["sunset_score"],
        "moon_phase": scores["moon_phase"],
        "fog_forecast": fog,
        "twilight_phases": twilight,
        "recommended_shoot_time": best_time,
        "summary_text": summary,
        "updated_at": datetime.now(pytz.utc).isoformat()
    }

def get_prediction_scores(city_name, moon_data):
    API_KEY = VISUAL_CROSSING_API_KEY
    city_query = city_name.replace(" ", "%20").lower()
    safe_city_name = quote(f"{city_name}, CA")
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{safe_city_name}/today?unitGroup=us&include=days,hours,astronomy&key={API_KEY}&contentType=json"

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

        moon_val = moon_phase_value()
        moon_label = get_moon_phase_label(moon_val)

        return {
            "sunrise_score": sunrise_score,
            "sunset_score": sunset_score,
            "moon_phase": {
                "value": round(moon_val, 2),
                "label": moon_label,
                "moonrise": moon_data.get("moonrise"),
                "moonset": moon_data.get("moonset")
            }
        }

    except Exception as e:
        print(f"⚠️ Error fetching weather data for {city_name}: {e}")
        return {
            "sunrise_score": 5,
            "sunset_score": 5,
            "moon_phase": {
                "value": None,
                "label": "Unknown",
                "moonrise": moon_data.get("moonrise"),
                "moonset": moon_data.get("moonset")
            }
        }
def get_fog_forecast(city_slug):
    API_KEY = METEOSOURCE_API_KEY
    url = f"https://www.meteosource.com/api/v1/free/point?place_id={city_slug}&sections=hourly&timezone=auto&language=en&units=us&key={API_KEY}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        fog_data = []
        for hour in data.get("hourly", {}).get("data", [])[:12]:
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
        print(f"⚠️ Error fetching fog forecast for {city_slug}: {e}")
        return []

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

    # Build twilight windows
    twilight_windows = [
        {
            "label": "Civil Twilight",
            "start": sun_times["dawn"],
            "end": sun_times["sunrise"]
        },
        {
            "label": "Golden Hour",
            "start": sun_times["sunrise"],
            "end": sun_times["sunrise"] + timedelta(hours=1)
        }
    ]

    # Convert datetime to display strings
    formatted_windows = []
    recommended = None

    for window in twilight_windows:
        matching_fog = [
            f for f in fog_forecast
            if "fog_score" in f and f["fog_score"] is not None and
               parse_forecast_time(f["time"]) >= window["start"] and
               parse_forecast_time(f["time"]) <= window["end"]
        ]
        if matching_fog:
            avg_fog = sum(f["fog_score"] for f in matching_fog) / len(matching_fog)
            if recommended is None or avg_fog < recommended["fog_score"]:
                recommended = {
                    "time": window["start"].strftime("%-I:%M %p"),
                    "phase": window["label"],
                    "fog_score": round(avg_fog, 2)
                }
            fog_score = round(avg_fog, 2)
        else:
            fog_score = None

        formatted_windows.append({
            "label": window["label"],
            "start": window["start"].strftime("%-I:%M %p"),
            "end": window["end"].strftime("%-I:%M %p"),
            "avg_fog_score": fog_score
        })

    if recommended and recommended["fog_score"] <= 5:
        summary = (
            f"Best time to shoot: {recommended['time']} — "
            f"low fog ({recommended['fog_score']}) during {recommended['phase']}."
        )
    else:
        summary = "No optimal low-fog window during twilight today. Consider shooting at sunset or when fog clears."

    return formatted_windows, recommended, summary

def calculate_fog_score(visibility, cloud_cover):
    if cloud_cover is None:
        return None
    if visibility is None:
        return round(min(cloud_cover / 10, 10), 1)
    score = 10 - min(visibility, 10) + (cloud_cover / 20)
    return round(min(max(score, 0), 10), 1)

def get_moon_phase_label(value):
    if value is None:
        return "Unknown"
    val = (value % 29.53) / 29.53
    if val == 0 or val == 1:
        return "New Moon" if val == 0 else "Full Moon"
    elif 0 < val < 0.25:
        return "Waxing Crescent"
    elif val == 0.25:
        return "First Quarter"
    elif 0.25 < val < 0.5:
        return "Waxing Gibbous"
    elif val == 0.5:
        return "Full Moon"
    elif 0.5 < val < 0.75:
        return "Waning Gibbous"
    elif val == 0.75:
        return "Last Quarter"
    else:
        return "Waning Crescent"

def create_predictions_file():
    predictions = {}
    for city in cities:
        slug, city_data = get_city_data(city)
        predictions[slug] = city_data

    with open("predictions.json", "w") as f:
        json.dump(predictions, f, indent=2)

    print("✅ predictions.json created!")

if __name__ == "__main__":
    create_predictions_file()
