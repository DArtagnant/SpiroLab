import flet as ft
from flet import canvas as cv

from .math import cartesian_to_screen_coords
from .state_provider import auto_updated_canvas

def main(page: ft.Page):
    page.title = "Proof of Concept"

    # TODO
    cp = auto_updated_canvas()

    # [cv.Circle(*cartesian_to_screen_coords(0,0,page.width,page.height), 60)]

    page.add(
        ft.Container(
            cp,
            border_radius=5,
            width=float("inf"),
            expand=True,
        )
    )

    # cp.on_resized = lambda _: cp.update()

def render():
    ft.app(main)