import reflex as rx
import httpx
import logging
from typing import Any

WEATHER_CODES = {
    0: ("Clear sky", "sun"),
    1: ("Mainly clear", "sun"),
    2: ("Partly cloudy", "cloud-sun"),
    3: ("Overcast", "cloud"),
    45: ("Fog", "cloud-fog"),
    48: ("Depositing rime fog", "cloud-fog"),
    51: ("Drizzle: Light intensity", "cloud-drizzle"),
    53: ("Drizzle: Moderate intensity", "cloud-drizzle"),
    55: ("Drizzle: Dense intensity", "cloud-drizzle"),
    56: ("Freezing Drizzle: Light intensity", "cloud-drizzle"),
    57: ("Freezing Drizzle: Dense intensity", "cloud-drizzle"),
    61: ("Rain: Slight intensity", "cloud-rain"),
    63: ("Rain: Moderate intensity", "cloud-rain"),
    65: ("Rain: Heavy intensity", "cloud-rain-heavy"),
    66: ("Freezing Rain: Light intensity", "cloud-rain-heavy"),
    67: ("Freezing Rain: Heavy intensity", "cloud-rain-heavy"),
    71: ("Snow fall: Slight intensity", "cloud-snow"),
    73: ("Snow fall: Moderate intensity", "cloud-snow"),
    75: ("Snow fall: Heavy intensity", "cloud-snow"),
    77: ("Snow grains", "cloud-snow"),
    80: ("Rain showers: Slight intensity", "cloud-hail"),
    81: ("Rain showers: Moderate intensity", "cloud-hail"),
    82: ("Rain showers: Violent intensity", "cloud-hail"),
    85: ("Snow showers: Slight intensity", "cloud-snow"),
    86: ("Snow showers: Heavy intensity", "cloud-snow"),
    95: ("Thunderstorm", "cloud-lightning"),
    96: ("Thunderstorm with slight hail", "cloud-lightning"),
    99: ("Thunderstorm with heavy hail", "cloud-lightning"),
}


class WeatherState(rx.State):
    """State for the Weather module."""

    search_city: str = ""
    is_loading: bool = False
    error_message: str = ""
    weather_data: dict | None = None

    @rx.var
    def weather_icon(self) -> str:
        """Returns the icon for the current weather code."""
        if self.weather_data:
            return WEATHER_CODES.get(
                self.weather_data["weather_code"], ("unknown", "help-circle")
            )[1]
        return "help-circle"

    @rx.event
    async def get_weather(self, form_data: dict[str, Any]):
        """Fetches weather data for the given city."""
        city = form_data.get("city", "").strip()
        if not city:
            self.error_message = "Please enter a city name."
            return
        self.is_loading = True
        self.error_message = ""
        self.weather_data = None
        yield
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                geo_response = await client.get(
                    f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
                )
                geo_response.raise_for_status()
                geo_data = geo_response.json()
            if not geo_data.get("results"):
                self.error_message = f"Could not find city: {city}. Try another name."
                self.is_loading = False
                return
            location = geo_data["results"][0]
            latitude = location["latitude"]
            longitude = location["longitude"]
            city_name = location["name"]
            async with httpx.AsyncClient(timeout=10.0) as client:
                weather_response = await client.get(
                    f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m"
                )
                weather_response.raise_for_status()
                data = weather_response.json()
            current_weather = data["current"]
            weather_code = int(current_weather["weather_code"])
            description, _ = WEATHER_CODES.get(
                weather_code, ("Unknown weather code", "help-circle")
            )
            self.weather_data = {
                "city": city_name,
                "temperature": round(current_weather["temperature_2m"]),
                "humidity": int(current_weather["relative_humidity_2m"]),
                "wind_speed": round(current_weather["wind_speed_10m"]),
                "weather_code": weather_code,
                "weather_description": description,
            }
            self.error_message = ""
        except httpx.HTTPStatusError as e:
            logging.exception(f"Error fetching weather data: {e}")
            self.error_message = (
                "An error occurred while fetching data. Please try again."
            )
        except Exception as e:
            logging.exception(f"An unexpected error occurred: {e}")
            self.error_message = f"An unexpected error occurred: {e}"
        finally:
            self.is_loading = False
            self.search_city = ""