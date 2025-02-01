import flet as ft
from flet import canvas as cv

from .spirograph import render_spirograph
from .state_provider import centered_canvas

def main(page: ft.Page):
    page.title = "Proof of Concept"

    cp = centered_canvas(page)

    render_spirograph(
        cp,
        (0,0),
        125,
        200,
        0.4,
        0.25
    )

    render_spirograph(
        cp,
        (0,0),
        50,
        20,
        0.1,
        0.25
    )

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