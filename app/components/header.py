import reflex as rx


def header_component() -> rx.Component:
    """The header component for the InfoHub app."""
    return rx.el.header(
        rx.el.div(
            rx.el.div(
                rx.icon("sprout", class_name="h-8 w-8 text-indigo-500"),
                rx.el.h1(
                    "InfoHub",
                    class_name="text-2xl md:text-3xl font-bold text-gray-800 tracking-tighter",
                ),
                class_name="flex items-center gap-3",
            ),
            rx.el.p(
                "Your daily digest of practical information.",
                class_name="hidden md:block text-sm text-gray-500 font-medium",
            ),
            class_name="container mx-auto flex items-center justify-between p-4",
        ),
        class_name="w-full bg-white/80 backdrop-blur-md border-b border-gray-100 sticky top-0 z-50",
    )