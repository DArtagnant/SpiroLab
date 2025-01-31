import flet as ft
from flet import canvas as cv

from .state_provider import centered_canvas

def main(page: ft.Page):
    page.title = "Proof of Concept"

    # TODO
    cp = centered_canvas(page)
    cp.append(cv.Circle(0, 0, 20, ft.Paint(ft.Colors.GREEN)))

    page.add(
        ft.Container(
            cp,
            border_radius=5,
            width=float("inf"),
            expand=True,
        )
    )

def render():
    ft.app(main)