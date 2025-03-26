import flet as ft
from .centered_canvas import centered_canvas
from .spirograph import render_spirograph
from math import pi

def custom_spiro_page(page: ft.Page):
    cc = centered_canvas(page)

    custom_spiro_page_view = ft.View(
        route="personalisation",
        controls=[
            ft.Row([
                ft.Container(
                    cc,
                    expand= True,
                ),
                ft.Column([
                    ft.Text("Paramètres :", theme_style=ft.TextThemeStyle.HEADLINE_SMALL),
                    ft.Text("Rayon du grand cercle"),
                    large_radius := ft.Slider(label="{value}px", min=10, max=300, value=100),
                    ft.Text("Rayon du petit cercle"),
                    small_radius := ft.Slider(label="{value}px", min=10, max=300, value=30),
                    ft.Text("Fréquence du petit cercle"),
                    large_frequency := ft.Slider(label="{value}", min=5, max=100, value=25),
                    ft.Text("Fréquence du point"),
                    small_frequency := ft.Slider(label="{value}", min=5, max=100, value=50),
                    ft.Text("Tourner"),
                    turn := ft.Slider(label="{value}", min=0, max=2*pi, value=0),
                    ft.ElevatedButton("Exporter", )
                ],
                width=300)
            ],
            expand=True)
        ]
    )

    def recompute_spirograph(_):
        cc.remove_all()
        spiro_id = render_spirograph(
            cc,
            (0,0),
            float(large_radius.value),
            float(small_radius.value),
            int(large_frequency.value),
            int(small_frequency.value),
            75,
        )
        cc.rotations[spiro_id] = float(turn.value)
        cc.draw_once()
    
    large_radius.on_change = recompute_spirograph
    small_radius.on_change = recompute_spirograph
    large_frequency.on_change = recompute_spirograph
    small_frequency.on_change = recompute_spirograph
    turn.on_change = recompute_spirograph

    recompute_spirograph(None)
    return custom_spiro_page_view