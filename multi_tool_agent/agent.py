import datetime
import requests
from zoneinfo import ZoneInfo
from google.adk.agents import Agent

# ----------------------------------------
# CITY DATABASE
# ----------------------------------------

CITY_DATA = {
    "new york": {"lat": 40.7128, "lon": -74.0060, "tz": "America/New_York"},
    "los angeles": {"lat": 34.0522, "lon": -118.2437, "tz": "America/Los_Angeles"},
    "chicago": {"lat": 41.8781, "lon": -87.6298, "tz": "America/Chicago"},
    "houston": {"lat": 29.7604, "lon": -95.3698, "tz": "America/Chicago"},
    "phoenix": {"lat": 33.4484, "lon": -112.0740, "tz": "America/Phoenix"},
    "philadelphia": {"lat": 39.9526, "lon": -75.1652, "tz": "America/New_York"},
    "san antonio": {"lat": 29.4241, "lon": -98.4936, "tz": "America/Chicago"},
    "san diego": {"lat": 32.7157, "lon": -117.1611, "tz": "America/Los_Angeles"},
    "dallas": {"lat": 32.7767, "lon": -96.7970, "tz": "America/Chicago"},
    "san jose": {"lat": 37.3382, "lon": -121.8863, "tz": "America/Los_Angeles"},
    "london": {"lat": 51.5074, "lon": -0.1278, "tz": "Europe/London"},
    "paris": {"lat": 48.8566, "lon": 2.3522, "tz": "Europe/Paris"},
    "berlin": {"lat": 52.5200, "lon": 13.4050, "tz": "Europe/Berlin"},
    "madrid": {"lat": 40.4168, "lon": -3.7038, "tz": "Europe/Madrid"},
    "rome": {"lat": 41.9028, "lon": 12.4964, "tz": "Europe/Rome"},
    "moscow": {"lat": 55.7558, "lon": 37.6173, "tz": "Europe/Moscow"},
    "beijing": {"lat": 39.9042, "lon": 116.4074, "tz": "Asia/Shanghai"},
    "tokyo": {"lat": 35.6762, "lon": 139.6503, "tz": "Asia/Tokyo"},
    "seoul": {"lat": 37.5665, "lon": 126.9780, "tz": "Asia/Seoul"},
    "shanghai": {"lat": 31.2304, "lon": 121.4737, "tz": "Asia/Shanghai"},
    "hong kong": {"lat": 22.3193, "lon": 114.1694, "tz": "Asia/Hong_Kong"},
    "bangkok": {"lat": 13.7563, "lon": 100.5018, "tz": "Asia/Bangkok"},
    "singapore": {"lat": 1.3521, "lon": 103.8198, "tz": "Asia/Singapore"},
    "delhi": {"lat": 28.6139, "lon": 77.2090, "tz": "Asia/Kolkata"},
    "mumbai": {"lat": 19.0760, "lon": 72.8777, "tz": "Asia/Kolkata"},
    "buenos aires": {"lat": -34.6037, "lon": -58.3816, "tz": "America/Argentina/Buenos_Aires"},
    "sao paulo": {"lat": -23.5505, "lon": -46.6333, "tz": "America/Sao_Paulo"},
    "rio de janeiro": {"lat": -22.9068, "lon": -43.1729, "tz": "America/Sao_Paulo"},
    "cape town": {"lat": -33.9249, "lon": 18.4241, "tz": "Africa/Johannesburg"},
    "lagos": {"lat": 6.5244, "lon": 3.3792, "tz": "Africa/Lagos"},
    "nairobi": {"lat": -1.286389, "lon": 36.817223, "tz": "Africa/Nairobi"},
    "cairo": {"lat": 30.0444, "lon": 31.2357, "tz": "Africa/Cairo"},
    "istanbul": {"lat": 41.0082, "lon": 28.9784, "tz": "Europe/Istanbul"},
    "dubai": {"lat": 25.2048, "lon": 55.2708, "tz": "Asia/Dubai"},
    "karachi": {"lat": 24.8607, "lon": 67.0011, "tz": "Asia/Karachi"},
    "tehran": {"lat": 35.6892, "lon": 51.3890, "tz": "Asia/Tehran"},
    "baghdad": {"lat": 33.3152, "lon": 44.3661, "tz": "Asia/Baghdad"},
    "riyadh": {"lat": 24.7136, "lon": 46.6753, "tz": "Asia/Riyadh"},
    "mexico city": {"lat": 19.4326, "lon": -99.1332, "tz": "America/Mexico_City"},
    "toronto": {"lat": 43.6532, "lon": -79.3832, "tz": "America/Toronto"},
    "vancouver": {"lat": 49.2827, "lon": -123.1207, "tz": "America/Vancouver"},
    "montreal": {"lat": 45.5017, "lon": -73.5673, "tz": "America/Toronto"},
    "sydney": {"lat": -33.8688, "lon": 151.2093, "tz": "Australia/Sydney"},
    "melbourne": {"lat": -37.8136, "lon": 144.9631, "tz": "Australia/Melbourne"},
    "brisbane": {"lat": -27.4698, "lon": 153.0251, "tz": "Australia/Brisbane"},
    "perth": {"lat": -31.9505, "lon": 115.8605, "tz": "Australia/Perth"},
    "auckland": {"lat": -36.8485, "lon": 174.7633, "tz": "Pacific/Auckland"},
    "wellington": {"lat": -41.2865, "lon": 174.7762, "tz": "Pacific/Auckland"},
    "moscow": {"lat": 55.7558, "lon": 37.6173, "tz": "Europe/Moscow"},
    "saint petersburg": {"lat": 59.9343, "lon": 30.3351, "tz": "Europe/Moscow"},
    "vienna": {"lat": 48.2082, "lon": 16.3738, "tz": "Europe/Vienna"},
    "prague": {"lat": 50.0755, "lon": 14.4378, "tz": "Europe/Prague"},
    "budapest": {"lat": 47.4979, "lon": 19.0402, "tz": "Europe/Budapest"},
    "warsaw": {"lat": 52.2297, "lon": 21.0122, "tz": "Europe/Warsaw"},
    "oslo": {"lat": 59.9139, "lon": 10.7522, "tz": "Europe/Oslo"},
    "stockholm": {"lat": 59.3293, "lon": 18.0686, "tz": "Europe/Stockholm"},
    "copenhagen": {"lat": 55.6761, "lon": 12.5683, "tz": "Europe/Copenhagen"},
    "helsinki": {"lat": 60.1699, "lon": 24.9384, "tz": "Europe/Helsinki"},
    "athens": {"lat": 37.9838, "lon": 23.7275, "tz": "Europe/Athens"},
    "lisbon": {"lat": 38.7169, "lon": -9.1393, "tz": "Europe/Lisbon"},
    "dublin": {"lat": 53.3331, "lon": -6.2489, "tz": "Europe/Dublin"},
    "belgrade": {"lat": 44.8176, "lon": 20.4569, "tz": "Europe/Belgrade"},
    "zagreb": {"lat": 45.8150, "lon": 15.9785, "tz": "Europe/Zagreb"},
    "sarajevo": {"lat": 43.8563, "lon": 18.4131, "tz": "Europe/Sarajevo"},
    "skopje": {"lat": 41.9981, "lon": 21.4254, "tz": "Europe/Skopje"},
    "sofia": {"lat": 42.6977, "lon": 23.3219, "tz": "Europe/Sofia"},
    "bucharest": {"lat": 44.4268, "lon": 26.1025, "tz": "Europe/Bucharest"},
    "amsterdam": {"lat": 52.3676, "lon": 4.9041, "tz": "Europe/Amsterdam"},
    "brussels": {"lat": 50.8503, "lon": 4.3517, "tz": "Europe/Brussels"},
    "luxembourg": {"lat": 49.6117, "lon": 6.1319, "tz": "Europe/Luxembourg"},
    "monaco": {"lat": 43.7384, "lon": 7.4246, "tz": "Europe/Monaco"},
    "reykjavik": {"lat": 64.1355, "lon": -21.8954, "tz": "Atlantic/Reykjavik"},
    "tokyo": {"lat": 35.6762, "lon": 139.6503, "tz": "Asia/Tokyo"},
    "osaka": {"lat": 34.6937, "lon": 135.5023, "tz": "Asia/Tokyo"},
    "kyoto": {"lat": 35.0116, "lon": 135.7681, "tz": "Asia/Tokyo"},
    "beijing": {"lat": 39.9042, "lon": 116.4074, "tz": "Asia/Shanghai"},
    "shanghai": {"lat": 31.2304, "lon": 121.4737, "tz": "Asia/Shanghai"},
    "guangzhou": {"lat": 23.1291, "lon": 113.2644, "tz": "Asia/Shanghai"},
    "chongqing": {"lat": 29.4316, "lon": 106.9123, "tz": "Asia/Shanghai"},
}


# ----------------------------------------
# WEATHER CODE MAPPING (Open-Meteo)
# ----------------------------------------

WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Foggy",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Light rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Light snow",
    73: "Moderate snow",
    75: "Heavy snow",
    95: "Thunderstorm",
}


# ----------------------------------------
# TOOL: GET WEATHER
# ----------------------------------------

def get_weather(city: str) -> dict:
    """Retrieves live weather from Open-Meteo."""
    city_key = city.lower()

    if city_key not in CITY_DATA:
        return {"status": "error", "error_message": f"City '{city}' is not supported."}

    lat = CITY_DATA[city_key]["lat"]
    lon = CITY_DATA[city_key]["lon"]

    try:
        url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}&current_weather=true"
        )
        response = requests.get(url)
        data = response.json()

        if "current_weather" not in data:
            return {"status": "error", "error_message": "No weather data returned."}

        cw = data["current_weather"]
        temp = cw["temperature"]
        wind = cw["windspeed"]
        wcode = cw["weathercode"]
        description = WEATHER_CODES.get(wcode, "Unknown weather")

        report = (
            f"Weather in {city.title()}: {description}. "
            f"Temperature: {temp}°C. Windspeed: {wind} km/h."
        )

        return {"status": "success", "report": report}

    except Exception as e:
        return {"status": "error", "error_message": str(e)}


# ----------------------------------------
# TOOL: GET TIME
# ----------------------------------------

def get_current_time(city: str) -> dict:
    """Returns the current time in the specified city."""
    city_key = city.lower()

    if city_key not in CITY_DATA:
        return {"status": "error", "error_message": f"City '{city}' is not supported."}

    tz = ZoneInfo(CITY_DATA[city_key]["tz"])
    now = datetime.datetime.now(tz)
    report = f"The current time in {city.title()} is {now.strftime('%Y-%m-%d %H:%M:%S %Z%z')}"

    return {"status": "success", "report": report}


# ----------------------------------------
# ROOT AGENT
# ----------------------------------------

root_agent = Agent(
    name="weather_time_agent",
    model="gemini-2.5-flash",
    description="Agent that can answer questions about time and weather.",
    instruction=(
        "You are a helpful assistant that can provide the current time and live weather "
        "for any city supported by the tools `get_weather` and `get_current_time`. "
        "Always call these tools to get accurate data instead of guessing. "
        "Do not restrict yourself to any specific cities."
    ),
    tools=[get_weather, get_current_time],
)

