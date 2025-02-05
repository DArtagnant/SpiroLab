import flet as ft
from flet import canvas as cv

from .bar import settings_bar
from .state_provider import centered_canvas

def main(page: ft.Page):
    page.title = "Proof of Concept"

    cp = centered_canvas(lambda:page.height)
    cp.append(cv.Circle(10, 10, 10))
    appbar = settings_bar(page, cp)
    test = cv.Canvas([cv.Circle(10, 10, 10)], expand=True, height=None, width=None)
    test.on_resize = lambda e: print(f"resized : {e}", dir(test.parent), test.parent.__dict__)
    page.add(
        ft.Row(
            [
                appbar,
                cp
            ]
        )
    )

def render():
    ft.app(main)