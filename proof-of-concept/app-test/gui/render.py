import flet as ft
from flet import canvas as cv

from .math import cartesian_to_screen_coords

def main(page: ft.Page):
    page.title = "Proof of Concept"

    # TODO
    cp = cv.Canvas(
        [cv.Circle(*cartesian_to_screen_coords(0,0,cp.width,cp.height), 60)]
    )

    page.add(
        ft.Container(
            cp,
            border_radius=5,
            width=float("inf"),
            expand=True,
        )
    )

    cp.on_resized = lambda _: cp.update()

def render():
    ft.app(main)