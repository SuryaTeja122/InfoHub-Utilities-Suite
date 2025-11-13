import reflex as rx
import httpx
import logging
from typing import Any


class CurrencyState(rx.State):
    """State for the Currency Converter module."""

    is_loading: bool = False
    error_message: str = ""
    amount_inr: float = 100.0
    conversion_results: dict | None = None

    @rx.var
    def usd_amount(self) -> str:
        """Formatted USD conversion result."""
        if self.conversion_results and self.conversion_results.get("rates"):
            rate = self.conversion_results["rates"].get("USD", 0)
            return f"${self.amount_inr * rate:.2f}"
        return "$0.00"

    @rx.var
    def eur_amount(self) -> str:
        """Formatted EUR conversion result."""
        if self.conversion_results and self.conversion_results.get("rates"):
            rate = self.conversion_results["rates"].get("EUR", 0)
            return f"€{self.amount_inr * rate:.2f}"
        return "€0.00"

    @rx.event
    async def convert_currency(self, form_data: dict[str, Any]):
        """Converts INR to USD and EUR."""
        amount_str = str(form_data.get("amount", "100"))
        try:
            self.amount_inr = float(amount_str)
        except ValueError as e:
            logging.exception(f"Invalid amount provided: {e}")
            self.error_message = "Please enter a valid number."
            return
        self.is_loading = True
        self.error_message = ""
        yield
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get("https://open.er-api.com/v6/latest/INR")
                response.raise_for_status()
                data = response.json()
                self.conversion_results = data
                self.error_message = ""
        except httpx.HTTPStatusError as e:
            logging.exception(f"Error fetching currency data: {e}")
            self.error_message = (
                "Could not retrieve exchange rates. The service may be down."
            )
            self.conversion_results = None
        except Exception as e:
            logging.exception(f"An unexpected error occurred: {e}")
            self.error_message = "An unexpected error occurred while fetching rates."
            self.conversion_results = None
        finally:
            self.is_loading = False