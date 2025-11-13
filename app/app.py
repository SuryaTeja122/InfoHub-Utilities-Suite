import reflex as rx
from app.states.state import State
from app.components.header import header_component
from app.components.navigation import navigation_component
from app.components.weather import weather_component
from app.components.currency_converter import currency_converter
from app.components.quotes_generator import quotes_generator


def index() -> rx.Component:
    """The main page of the InfoHub application."""
    return rx.el.div(
        header_component(),
        rx.el.main(
            navigation_component(),
            rx.el.div(
                rx.match(
                    State.active_tab,
                    ("Weather", weather_component()),
                    ("Currency", currency_converter()),
                    ("Quotes", quotes_generator()),
                    weather_component(),
                ),
                class_name="container mx-auto max-w-3xl px-4",
            ),
            class_name="flex-grow",
        ),
        rx.el.footer(
            rx.el.p(
                "Built with ",
                rx.el.a(
                    "Reflex",
                    href="https://reflex.dev",
                    target="_blank",
                    class_name="text-indigo-500 hover:underline font-semibold",
                ),
                " & ",
                class_name="text-sm text-gray-500",
            ),
            class_name="text-center p-4 text-gray-500",
        ),
        class_name="min-h-screen bg-gray-50 font-['Raleway'] flex flex-col",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Raleway:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, route="/")