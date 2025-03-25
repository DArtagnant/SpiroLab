import flet as ft
from time import sleep

from .home_page import home_page
from .bar import settings_bar
from .centered_canvas import centered_canvas

def main(page: ft.Page):
    page.title = "SpiroLab"

    page.fonts = {
        "monospace": "./static_data/Monospace.ttf"
    }

    cp = centered_canvas(page)
    bar = settings_bar(page, cp)
    # home_page(page) # TODO, fix le passage de la home_page au reste
    page.add(
        bar,
        ft.Container(
            cp,
            border_radius=5,
            width=float("inf"),
            expand=True,
        ),
    )
    
