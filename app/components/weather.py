import reflex as rx
from app.states.weather_state import WeatherState
from app.components.placeholders import skeleton_card


def weather_search_form() -> rx.Component:
    """The search form for the weather module."""
    return rx.el.form(
        rx.el.div(
            rx.el.input(
                placeholder="E.g., New York, London, Tokyo",
                name="city",
                type="search",
                class_name="flex-grow p-3 text-base text-gray-700 bg-white border border-gray-300 rounded-l-lg focus:ring-2 focus:ring-indigo-400 focus:border-transparent outline-none transition-shadow",
            ),
            rx.el.button(
                rx.icon("search", class_name="h-5 w-5"),
                "Search",
                type="submit",
                class_name="flex items-center gap-2 px-4 py-3 bg-indigo-500 text-white font-semibold rounded-r-lg hover:bg-indigo-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors duration-200 disabled:opacity-50",
                disabled=WeatherState.is_loading,
            ),
            class_name="flex items-center shadow-sm rounded-lg",
        ),
        on_submit=WeatherState.get_weather,
    )


def weather_display() -> rx.Component:
    """Displays the weather data or appropriate states."""
    return rx.el.div(
        rx.cond(
            WeatherState.is_loading,
            skeleton_card(),
            rx.cond(
                WeatherState.error_message != "",
                rx.el.div(
                    rx.icon(
                        "flag_triangle_right",
                        class_name="h-12 w-12 text-yellow-500 mx-auto",
                    ),
                    rx.el.h3(
                        "Error", class_name="mt-4 text-xl font-semibold text-gray-800"
                    ),
                    rx.el.p(
                        WeatherState.error_message,
                        class_name="mt-2 text-center text-gray-600",
                    ),
                    class_name="p-8 text-center bg-white border border-gray-100 rounded-2xl shadow-sm",
                ),
                rx.cond(
                    WeatherState.weather_data.is_not_none(),
                    rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                rx.el.h2(
                                    WeatherState.weather_data["city"],
                                    class_name="text-2xl font-bold text-gray-800 tracking-tight",
                                ),
                                rx.el.p(
                                    WeatherState.weather_data["weather_description"],
                                    class_name="text-gray-500 font-medium",
                                ),
                                class_name="flex-grow",
                            ),
                            rx.icon(
                                WeatherState.weather_icon,
                                class_name="h-16 w-16 text-indigo-500",
                            ),
                            class_name="flex items-start justify-between",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.div(
                                    rx.el.p(
                                        "Temperature",
                                        class_name="text-sm text-gray-500 font-medium",
                                    ),
                                    rx.el.p(
                                        f"{WeatherState.weather_data['temperature']}°C",
                                        class_name="text-2xl font-semibold text-gray-800",
                                    ),
                                    class_name="text-center p-4 bg-gray-50 rounded-lg",
                                ),
                                rx.el.div(
                                    rx.el.p(
                                        "Humidity",
                                        class_name="text-sm text-gray-500 font-medium",
                                    ),
                                    rx.el.p(
                                        f"{WeatherState.weather_data['humidity']}%",
                                        class_name="text-2xl font-semibold text-gray-800",
                                    ),
                                    class_name="text-center p-4 bg-gray-50 rounded-lg",
                                ),
                                rx.el.div(
                                    rx.el.p(
                                        "Wind Speed",
                                        class_name="text-sm text-gray-500 font-medium",
                                    ),
                                    rx.el.p(
                                        f"{WeatherState.weather_data['wind_speed']} km/h",
                                        class_name="text-2xl font-semibold text-gray-800",
                                    ),
                                    class_name="text-center p-4 bg-gray-50 rounded-lg",
                                ),
                                class_name="grid grid-cols-3 gap-4 mt-6",
                            ),
                            class_name="mt-6",
                        ),
                        class_name="p-6 md:p-8 bg-white border border-gray-100 rounded-2xl shadow-sm",
                    ),
                    rx.el.div(
                        rx.icon(
                            "cloud-sun", class_name="h-12 w-12 text-gray-400 mx-auto"
                        ),
                        rx.el.h3(
                            "Check the Weather",
                            class_name="mt-4 text-xl font-semibold text-gray-800",
                        ),
                        rx.el.p(
                            "Enter a city name above to get the current weather conditions.",
                            class_name="mt-2 text-center text-gray-600",
                        ),
                        class_name="p-8 text-center bg-white border border-gray-100 rounded-2xl shadow-sm",
                    ),
                ),
            ),
        ),
        class_name="mt-6",
    )


def weather_component() -> rx.Component:
    """The main component for the Weather module."""
    return rx.el.div(weather_search_form(), weather_display(), class_name="w-full")