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
            float(large_angular_velocity.value),
            float(small_angular_velocity.value),
            float(resolution.value),
        )
        page.update()

    # Faire une classe NumberInputField ? (ce serait mieux mais bon programme et tout)
    large_radius = ft.TextField(label="Rayon du grand cercle", value=125)
    small_radius = ft.TextField(label="Rayon du petit cercle", value=200)

    large_angular_velocity = ft.TextField(label="Vitesse du petit cercle", value=0.4)
    small_angular_velocity = ft.TextField(label="Vitesse du point", value=0.25)

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
            large_angular_velocity,
            small_angular_velocity,
        ]),
        ft.Column([
            resolution,
            b,
        ])
    ])