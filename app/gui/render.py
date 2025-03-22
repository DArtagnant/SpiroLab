import flet as ft
from time import sleep

from .home_page import home_page
from .centered_canvas import centered_canvas

def main(page: ft.Page):
    page.title = "SpiroLab"

    # cp = centered_canvas(page)
    home_page(page)
    # page.add(
    #     # ft.Container(
    #     #     cp,
    #     #     border_radius=5,
    #     #     width=float("inf"),
    #     #     expand=True,
    #     # ),
    # )



def render():
    ft.app(main)