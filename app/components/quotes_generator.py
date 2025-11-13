import reflex as rx
from app.states.quote_state import QuoteState
from app.components.placeholders import skeleton_card


def quotes_display() -> rx.Component:
    """Displays the motivational quote or other states."""
    return rx.el.div(
        rx.cond(
            QuoteState.is_loading,
            skeleton_card(),
            rx.cond(
                QuoteState.error_message != "",
                rx.el.div(
                    rx.icon(
                        "flag_triangle_right",
                        class_name="h-12 w-12 text-yellow-500 mx-auto",
                    ),
                    rx.el.h3(
                        "Error", class_name="mt-4 text-xl font-semibold text-gray-800"
                    ),
                    rx.el.p(
                        QuoteState.error_message,
                        class_name="mt-2 text-center text-gray-600",
                    ),
                    class_name="p-8 text-center bg-white border border-gray-100 rounded-2xl shadow-sm",
                ),
                rx.cond(
                    QuoteState.quote.is_not_none(),
                    rx.el.div(
                        rx.el.blockquote(
                            rx.el.p(
                                f'''"{QuoteState.quote["text"]}"''',
                                class_name="text-xl md:text-2xl font-medium text-gray-800 leading-relaxed",
                            ),
                            class_name="relative mb-4",
                        ),
                        rx.el.cite(
                            f"- {QuoteState.quote['author']}",
                            class_name="text-gray-500 font-medium not-italic",
                        ),
                        class_name="p-6 md:p-8 bg-white border border-gray-100 rounded-2xl shadow-sm text-center transition-all duration-300",
                    ),
                    skeleton_card(),
                ),
            ),
        ),
        class_name="w-full transition-opacity duration-500",
    )


def quotes_generator() -> rx.Component:
    """The main component for the Quotes module."""
    return rx.el.div(
        quotes_display(),
        rx.el.div(
            rx.el.button(
                rx.icon("refresh-cw", class_name="h-5 w-5"),
                "New Quote",
                on_click=QuoteState.get_new_quote,
                class_name="flex items-center gap-2 px-4 py-3 bg-indigo-500 text-white font-semibold rounded-lg hover:bg-indigo-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all duration-300 transform hover:scale-105 active:scale-98 disabled:opacity-50",
                disabled=QuoteState.is_loading,
            ),
            class_name="flex justify-center mt-6",
        ),
        class_name="w-full",
        on_mount=QuoteState.get_new_quote,
    )