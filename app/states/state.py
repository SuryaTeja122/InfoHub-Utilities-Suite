import reflex as rx
from typing import Literal
from app.states.quote_state import QuoteState

TabName = Literal["Weather", "Currency", "Quotes"]


class State(rx.State):
    """The main state for the InfoHub application."""

    active_tab: TabName = "Weather"
    tabs: list[TabName] = ["Weather", "Currency", "Quotes"]

    @rx.event
    def set_active_tab(self, tab: TabName):
        """Sets the active tab and triggers side effects if necessary."""
        self.active_tab = tab