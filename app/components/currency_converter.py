import reflex as rx
from app.states.currency_state import CurrencyState
from app.components.placeholders import skeleton_card


def currency_form() -> rx.Component:
    """The form for currency conversion."""
    return rx.el.form(
        rx.el.div(
            rx.el.input(
                placeholder="Amount in INR",
                name="amount",
                default_value=CurrencyState.amount_inr.to_string(),
                type="number",
                class_name="flex-grow p-3 text-base text-gray-700 bg-white border border-gray-300 rounded-l-lg focus:ring-2 focus:ring-indigo-400 focus:border-transparent outline-none transition-shadow",
            ),
            rx.el.button(
                rx.icon("arrow-right-left", class_name="h-5 w-5"),
                "Convert",
                type="submit",
                class_name="flex items-center gap-2 px-4 py-3 bg-indigo-500 text-white font-semibold rounded-r-lg hover:bg-indigo-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors duration-200 disabled:opacity-50",
                disabled=CurrencyState.is_loading,
            ),
            class_name="flex items-center shadow-sm rounded-lg",
        ),
        on_submit=CurrencyState.convert_currency,
    )


def currency_display() -> rx.Component:
    """Displays the currency conversion results or other states."""
    return rx.el.div(
        rx.cond(
            CurrencyState.is_loading,
            skeleton_card(),
            rx.cond(
                CurrencyState.error_message != "",
                rx.el.div(
                    rx.icon(
                        "badge_alert", class_name="h-12 w-12 text-yellow-500 mx-auto"
                    ),
                    rx.el.h3(
                        "Error", class_name="mt-4 text-xl font-semibold text-gray-800"
                    ),
                    rx.el.p(
                        CurrencyState.error_message,
                        class_name="mt-2 text-center text-gray-600",
                    ),
                    class_name="p-8 text-center bg-white border border-gray-100 rounded-2xl shadow-sm",
                ),
                rx.cond(
                    CurrencyState.conversion_results.is_not_none(),
                    rx.el.div(
                        rx.el.div(
                            rx.el.h2(
                                f" INR {CurrencyState.amount_inr.to_string()} equals",
                                class_name="text-2xl font-bold text-gray-800 tracking-tight",
                            ),
                            class_name="flex items-start justify-between mb-6",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.p(
                                    "US Dollar",
                                    class_name="text-sm text-gray-500 font-medium",
                                ),
                                rx.el.p(
                                    CurrencyState.usd_amount,
                                    class_name="text-3xl font-semibold text-indigo-600",
                                ),
                                class_name="text-center p-4 bg-gray-50 rounded-lg",
                            ),
                            rx.el.div(
                                rx.el.p(
                                    "Euro",
                                    class_name="text-sm text-gray-500 font-medium",
                                ),
                                rx.el.p(
                                    CurrencyState.eur_amount,
                                    class_name="text-3xl font-semibold text-indigo-600",
                                ),
                                class_name="text-center p-4 bg-gray-50 rounded-lg",
                            ),
                            class_name="grid grid-cols-2 gap-4",
                        ),
                        class_name="p-6 md:p-8 bg-white border border-gray-100 rounded-2xl shadow-sm",
                    ),
                    rx.el.div(
                        rx.icon(
                            "banknote", class_name="h-12 w-12 text-gray-400 mx-auto"
                        ),
                        rx.el.h3(
                            "Currency Converter",
                            class_name="mt-4 text-xl font-semibold text-gray-800",
                        ),
                        rx.el.p(
                            "Enter an amount in INR to convert it to USD and EUR.",
                            class_name="mt-2 text-center text-gray-600",
                        ),
                        class_name="p-8 text-center bg-white border border-gray-100 rounded-2xl shadow-sm",
                    ),
                ),
            ),
        ),
        class_name="mt-6",
    )


def currency_converter() -> rx.Component:
    """The main component for the Currency Converter module."""
    return rx.el.div(
        currency_form(),
        currency_display(),
        class_name="w-full",
        on_mount=CurrencyState.convert_currency({"amount": "100"}),
    )