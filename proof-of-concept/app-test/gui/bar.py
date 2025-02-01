import flet as ft
from .spirograph import render_spirograph

def settings_bar(page: ft.Page, cv: ft.canvas.Canvas):
    def recompute_spirograph(_):
        cv.shapes = []
        render_spirograph(
            cv,
            (0,0),
            float(large_radius.value),
            float(small_radius.value),
            float(large_angular_velocity.value),
            float(small_angular_velocity.value),
        )
        page.update()

    # Faire une classe NumberInputField ? (ce serait mieux mais bon programme et tout)
    large_radius = ft.TextField(label="Rayon du grand cercle", value=125)
    small_radius = ft.TextField(label="Rayon du petit cercle", value=200)

    large_angular_velocity = ft.TextField(label="Vitesse du petit cercle", value=0.4)
    small_angular_velocity = ft.TextField(label="Vitesse du point", value=0.25)

    b = ft.ElevatedButton(text="Afficher", on_click=recompute_spirograph)

    recompute_spirograph(0) # Affiche le spirographe par défaut

    return ft.Column(
        [large_radius,
        small_radius,
        large_angular_velocity,
        small_angular_velocity,
        b]
    )