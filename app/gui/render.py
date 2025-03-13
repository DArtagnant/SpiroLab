import flet as ft
import flet_audio_recorder as far
from flet import canvas as cv

from time import sleep

from .bar import settings_bar
from .state_provider import centered_canvas
from .spirograph import render_spirographs_from_data
from formule import fourier
from audio import test_audio
from scipy.fft import rfft

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
    print("called")

def render():
    ft.app(main)