import flet as ft
from .spirograph import render_spirograph

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

    # Faire une classe NumberInputField ? (ce serait mieux mais bon programme et tout)
    large_radius = ft.TextField(label="Rayon du grand cercle", value=125)
    small_radius = ft.TextField(label="Rayon du petit cercle", value=200)

    large_frequency = ft.TextField(label="Fréquence du petit cercle", value=100)
    small_frequency = ft.TextField(label="Fréquence du point", value=50)

    resolution = ft.TextField(label="Resolution", value=50)

    b = ft.ElevatedButton(text="Afficher", on_click=recompute_spirograph)

    # Automatisation de la génération du spirographe à chaque pression de la touche 'Enter'
    def on_keyboard(e: ft.KeyboardEvent):
        if e.key == 'Enter':
            recompute_spirograph('rien')
        elif e.key == 'M':
            recompute_spirograph(0) # Affiche le spirographe par défaut


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