import flet as ft
from .spirograph import render_spirograph
from audio.getter import read_wav
from time import sleep
from numpy import real, imag
from random import randint
from formule import create_svg_for

max_spiros = 5

def settings_bar(page: ft.Page, canvas: ft.canvas.Canvas):
    def recompute_spirograph(_):
        canvas.shapes = []
        render_spirograph(
            canvas,
            (0,0),
            float(large_radius.value),
            float(small_radius.value),
            int(large_frequency.value),
            int(small_frequency.value),
            float(resolution.value),
        )
        page.update()
        create_svg_for(canvas.shapes, "a.svg", height= 1000, width= 1000, line_width= 2)

    def recompute_spirograph_from_wav():
        file = read_wav()
        print(len(file))
        for i in range(len(file)):
            if i%max_spiros == 0:
                canvas.shapes = []
            data = file[i]
            # TODO : fix les valeurs de "normalisation" un peu hasardeuses
            render_spirograph(
                canvas,
                (randint(-400, 400), randint(-200, 200)),
                abs(data[0])*3 + 5, 
                abs(data[1])*3 + 5, 
                int(data[2])%50 + 1,
                int(data[3])%50 + 1, 
                abs(float(data[4]))/10 + 40 # TODO : plus clean : Empêche la précision d'être trop grande ou petite 
            )
            page.update()
        

    # Faire une classe NumberInputField ? (ce serait mieux mais bon programme et tout)
    large_radius = ft.TextField(label="Rayon du grand cercle", value=125)
    small_radius = ft.TextField(label="Rayon du petit cercle", value=200)

    large_frequency = ft.TextField(label="Fréquence du petit cercle", value=100)
    small_frequency = ft.TextField(label="Fréquence du point", value=50)

    resolution = ft.TextField(label="Resolution", value=50)

    b = ft.ElevatedButton(text="Afficher", on_click=recompute_spirograph)

    # Automatisation de la génération du spirographe à chaque pression de la touche 'Enter'
    def on_keyboard(e: ft.KeyboardEvent):
        if e.key == 'R':
            recompute_spirograph_from_wav()
        if e.key == 'M':
            recompute_spirograph("") # Affiche le spirographe par défaut


    page.on_keyboard_event = on_keyboard

    # recompute_spirograph(0) # Affiche le spirographe par défaut

    return ft.Row([
        ft.Column([
            large_radius,
            small_radius,
        ]),
        ft.Column([
            large_frequency,
            small_frequency,
        ]),
        ft.Column([
            resolution,
            b,
        ])
    ])