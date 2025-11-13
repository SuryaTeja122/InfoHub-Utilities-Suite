import reflex as rx
import httpx
import logging
import random
from typing import Any


class QuoteState(rx.State):
    """State for the Motivational Quotes module."""

    is_loading: bool = False
    error_message: str = ""
    quote: dict[str, str] | None = None
    _local_quotes: list[dict[str, str]] = [
        {
            "text": "The only way to do great work is to love what you do.",
            "author": "Steve Jobs",
        },
        {
            "text": "Believe you can and you're halfway there.",
            "author": "Theodore Roosevelt",
        },
        {
            "text": "The future belongs to those who believe in the beauty of their dreams.",
            "author": "Eleanor Roosevelt",
        },
        {
            "text": "Strive not to be a success, but rather to be of value.",
            "author": "Albert Einstein",
        },
        {
            "text": "The mind is everything. What you think you become.",
            "author": "Buddha",
        },
        {"text": "An unexamined life is not worth living.", "author": "Socrates"},
        {
            "text": "Your time is limited, don't waste it living someone else's life.",
            "author": "Steve Jobs",
        },
        {
            "text": "The best way to predict the future is to create it.",
            "author": "Peter Drucker",
        },
        {
            "text": "Success is not final, failure is not fatal: it is the courage to continue that counts.",
            "author": "Winston Churchill",
        },
        {
            "text": "It does not matter how slowly you go as long as you do not stop.",
            "author": "Confucius",
        },
    ]

    def _get_fallback_quote(self):
        """Selects a random quote from the local list."""
        self.quote = random.choice(self._local_quotes)
        self.error_message = ""

    @rx.event
    async def get_new_quote(self):
        """Fetches a new random quote, with a fallback to local quotes."""
        self.is_loading = True
        self.error_message = ""
        yield
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get("https://zenquotes.io/api/random")
                response.raise_for_status()
                data = response.json()
            if data:
                quote_data = data[0]
                self.quote = {
                    "text": quote_data.get("q", ""),
                    "author": quote_data.get("a", "Unknown"),
                }
                self.error_message = ""
            else:
                self._get_fallback_quote()
        except httpx.HTTPStatusError as e:
            logging.exception(f"API Error fetching quote: {e}. Using fallback.")
            self._get_fallback_quote()
        except Exception as e:
            logging.exception(f"Unexpected error fetching quote: {e}. Using fallback.")
            self._get_fallback_quote()
        finally:
            self.is_loading = False