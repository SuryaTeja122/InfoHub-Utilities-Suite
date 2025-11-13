import reflex as rx


def skeleton_card() -> rx.Component:
    """A skeleton loading card for placeholder content."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(class_name="h-6 w-1/3 bg-gray-200 rounded-md"),
            class_name="flex items-center justify-between mb-6",
        ),
        rx.el.div(
            rx.el.div(class_name="h-4 w-full bg-gray-200 rounded-md"),
            rx.el.div(class_name="h-4 w-5/6 bg-gray-200 rounded-md"),
            rx.el.div(class_name="h-4 w-3/4 bg-gray-200 rounded-md"),
            class_name="space-y-3",
        ),
        rx.el.div(
            rx.el.div(class_name="h-10 w-24 bg-gray-200 rounded-lg"), class_name="mt-8"
        ),
        class_name="p-6 md:p-8 bg-white border border-gray-100 rounded-2xl shadow-sm animate-pulse w-full",
    )