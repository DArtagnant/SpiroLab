import flet as ft
from flet import canvas as cv


from .bar import settings_bar
from .state_provider import centered_canvas

def main(page: ft.Page):
    page.title = "Proof of Concept"

    cp = centered_canvas(page)
    appbar = settings_bar(page, cp)

    page.add(
        appbar,
        ft.Container(
            cp,
            border_radius=5,
            width=float("inf"),
            expand=True,
        ),
    )

def render():
    ft.app(main)