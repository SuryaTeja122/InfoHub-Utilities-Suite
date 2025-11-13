import reflex as rx
from app.states.state import State


def navigation_component() -> rx.Component:
    """The navigation tabs component."""
    return rx.el.nav(
        rx.el.div(
            rx.foreach(
                State.tabs,
                lambda tab: rx.el.button(
                    tab,
                    on_click=lambda: State.set_active_tab(tab),
                    class_name=rx.cond(
                        State.active_tab == tab,
                        "px-4 py-2 rounded-lg text-sm font-semibold text-white bg-indigo-500 shadow-md transition-all duration-300 transform scale-105",
                        "px-4 py-2 rounded-lg text-sm font-semibold text-gray-600 bg-gray-100 hover:bg-gray-200 hover:text-gray-800 transition-all duration-300 transform hover:scale-105 active:scale-98",
                    ),
                ),
            ),
            class_name="flex items-center gap-2 md:gap-4 p-2 bg-gray-50 border border-gray-200 rounded-xl w-fit",
        ),
        class_name="flex justify-center my-6 md:my-8",
    )