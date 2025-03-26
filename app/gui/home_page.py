import flet as ft
from time import sleep
from .centered_canvas import centered_canvas
from .spirograph import render_spirograph
from formule.easing import *
from formule.colors_creator import smooth_color_generator
from itertools import cycle

LOGO ="""
███████╗██████╗ ██╗██████╗  ██████╗ ██╗      █████╗ ██████╗ 
██╔════╝██╔══██╗██║██╔══██╗██╔═══██╗██║     ██╔══██╗██╔══██╗
███████╗██████╔╝██║██████╔╝██║   ██║██║     ███████║██████╔╝
╚════██║██╔═══╝ ██║██╔══██╗██║   ██║██║     ██╔══██║██╔══██╗
███████║██║     ██║██║  ██║╚██████╔╝███████╗██║  ██║██████╔╝
╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═════╝ 
"""


def home_page(page: ft.Page, spiro_should_turn: bool = False):

    logo_text = ft.Text(
        spans=[
            ft.TextSpan(
                LOGO,
                ft.TextStyle(
                    font_family="monospace",
                    size=18,
                    foreground=ft.Paint(
                        gradient= (paint_color := ft.PaintLinearGradient(
                            begin=(0, 0),
                            end=(page.width, page.height),
                            colors=[ft.Colors.BLUE, ft.Colors.LIGHT_BLUE, ft.Colors.LIGHT_GREEN, ft.Colors.GREEN],
                            color_stops=[0.0, 0.25, 0.5, 0.75]
                        ))
                    )
                )
            )
        ],
    )

    page.add(ft.Row([
                ft.Stack([
                    canvas_container := ft.Container(
                        canvas := centered_canvas(page),
                        opacity=0,
                    ),
                    ft.Column([
                        logo_text,
                        text_bienvenue := ft.Text("Bienvenue dans SpiroLab !", size=18, opacity=1),
                        bas := ft.Container(
                            ft.Text("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut \n labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation \n ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in \n reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat \n non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
                                    text_align=ft.TextAlign.CENTER),
                            height=0,
                            opacity=0
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
            ])
        ],
        alignment= ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
    ))

    page.floating_action_button = ft.FloatingActionButton(text="Commençons", icon=ft.Icons.ADD, on_click=lambda _: print("TODO"), opacity=0)

    def animation_color():
        nonlocal paint_color
        colors = [ft.Colors.BLUE, ft.Colors.LIGHT_BLUE, ft.Colors.LIGHT_GREEN, ft.Colors.GREEN, ft.Colors.ORANGE, ft.Colors.RED, ft.Colors.PINK, ft.Colors.DEEP_PURPLE]
        while True:
            paint_color.color_stops = list(e+0.01 for e in paint_color.color_stops)
            if paint_color.color_stops[-1] > 1:
                val = paint_color.color_stops[-1]
                del paint_color.color_stops[-1]
                del paint_color.colors[-1]
                paint_color.color_stops.insert(0, val - 1)
                paint_color.colors.insert(0, colors[(colors.index(paint_color.colors[0]) + 1) % len(colors)])
            page.update()
            sleep(0.1)

    def animate_title_position():
        nonlocal bas, text_bienvenue, page
        sleep(2) # TEMPS ICI
        start_height = 0
        end_height = 400
        total_height = end_height - start_height
        start_opacity = 1
        n_steps = 1000
        for step in range(n_steps):
            t = step / n_steps
            bas.height = start_height + ease_in_out_cubic(t) * total_height
            bas.opacity = ease_out_sine(t**3)
            page.floating_action_button.opacity = ease_in_sine(t)
            text_bienvenue.opacity = start_opacity - min(1, ease_in_sine(t*2))
            #print(bas.height)
            page.update()
            sleep(0.005)
    
    def animate_spiro_background():
        nonlocal canvas
        sleep(8)
        colors_pastel1 = ("#ACDDDE", "#CAF1DE", "#E1F8DC")
        colors_pastel2 = ("#FEF8DD", "#FFE7C7", "#F7D8BA")
        s1 = render_spirograph(canvas, (-100, -100), 200, 75, 10, 50, 10, 2, lambda nb_points: cycle(smooth_color_generator(colors_pastel1, int(nb_points/2), easing=ease_in_out_cubic)))
        s2 = render_spirograph(canvas, (700, -600), 350, 100, 10, 30, 10, 2, lambda nb_points: cycle(smooth_color_generator(colors_pastel2, int(nb_points/2))))
        if spiro_should_turn:
            canvas.rotations[s1] = 0
            canvas.rotations[s2] = 0
            while True:
                canvas.rotations[s1] += 0.005
                canvas.rotations[s2] += 0.003
                canvas.draw_once()
                sleep(0.2)
    
    def animate_spiro_show():
        nonlocal canvas_container
        sleep(8)
        n_steps = 1000
        for step in range(n_steps):
            t = step / n_steps
            canvas_container.opacity = ease_in_sine(t)
            page.update()
            sleep(0.005)

    page.run_thread(animation_color)
    page.run_thread(animate_title_position)
    page.run_thread(animate_spiro_background)
    page.run_thread(animate_spiro_show)

