import urllib.request
import urllib.parse
import json


def get_city(city):
    url = "https://geocoding-api.open-meteo.com/v1/search?"
    params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    url += urllib.parse.urlencode(params)

    with urllib.request.urlopen(url, timeout=10) as response:
        data = json.loads(response.read().decode("utf-8"))

    if "results" not in data:
        return None

    return data["results"][0]


def get_weather(latitude, longitude):
    url = "https://api.open-meteo.com/v1/forecast?"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "apparent_temperature,"
            "weather_code,"
            "wind_speed_10m"
        ),
        "timezone": "auto"
    }

    url += urllib.parse.urlencode(params)

    with urllib.request.urlopen(url, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


def weather_description(code):
    weather = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        80: "Rain showers",
        81: "Moderate rain showers",
        82: "Heavy rain showers",
        95: "Thunderstorm"
    }

    return weather.get(code, "Other weather conditions")


def main():
    print("\n===== WEATHER DATA CLI =====")

    while True:
        city = input("\nEnter city name (or 'exit'): ").strip()

        if city.lower() == "exit":
            print("Thank you for using Weather CLI!")
            break

        if not city:
            print("Please enter a city name.")
            continue

        try:
            location = get_city(city)

            if location is None:
                print("City not found. Try another city.")
                continue

            data = get_weather(
                location["latitude"],
                location["longitude"]
            )

            current = data["current"]

            print("\n------ WEATHER REPORT ------")
            print("City:", location["name"])
            print("Country:", location.get("country", "Unknown"))
            print("Temperature:", current["temperature_2m"], "°C")
            print("Feels Like:", current["apparent_temperature"], "°C")
            print("Humidity:", current["relative_humidity_2m"], "%")
            print("Wind Speed:", current["wind_speed_10m"], "km/h")
            print(
                "Condition:",
                weather_description(current["weather_code"])
            )
            print("Local Time:", current["time"])
            print("---------------------------")

        except Exception as error:
            print("Unable to fetch weather data.")
            print("Check your internet connection and try again.")
            print("Error:", error)


if __name__ == "__main__":
    main()