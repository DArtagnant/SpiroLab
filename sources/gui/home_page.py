import flet as ft
from time import sleep
from .components.centered_canvas import centered_canvas
from .components.spirograph import render_spirograph
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


def home_page(page: ft.Page, go_to_view_record, spiro_should_turn: bool = False) -> ft.View:
    page.current_view_name = "home_page"
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

    home_page_view = ft.View(
        route= "/home",
        controls=[ft.Row([
                ft.Stack([
                    canvas_container := ft.Container(
                        canvas := centered_canvas(page),
                        opacity=0,
                    ),
                    ft.Column([
                        logo_text,
                        text_bienvenue := ft.Text("Bienvenue dans SpiroLab !", size=23, opacity=1),
                        bas := ft.Container(
                            ft.Text("Une expérience musicale et visuelle\nAdmirez la géométrie des ondes acoustiques.\nFaites danser les courbes et les couleurs sur les fréquences de votre voix ou de vos musiques préférées.",
                                    text_align=ft.TextAlign.CENTER,
                                    size=18,
                                ),
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
    )]
    )

    home_page_view.floating_action_button = ft.FloatingActionButton(text="Commencer", icon=ft.Icons.ARROW_FORWARD, on_click=go_to_view_record, opacity=0)


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
            if page.current_view_name == "home_page":
                home_page_view.update()
            else:
                return
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
            home_page_view.floating_action_button.opacity = ease_in_sine(t)
            text_bienvenue.opacity = start_opacity - min(1, ease_in_sine(t*2))
            if page.current_view_name == "home_page":
                home_page_view.update()
            else:
                return
            sleep(0.005)
    
    def animate_spiro_background():
        nonlocal canvas
        sleep(8)
        colors_pastel1 = ("#76BA71", "#EDE687", "#F7B05E", "#E67A73", "#99408A")
        colors_pastel2 = ("#8E3600", "#D05903", "#F56517", "#FDAB04", "#EEC5A2", "#492E0B")
        s1 = render_spirograph(canvas, (-200, 0), 150, 200, 60, 132, 10, 2, lambda nb_points: cycle(smooth_color_generator(colors_pastel1, int(nb_points/2), easing=ease_in_out_cubic)))
        s2 = render_spirograph(canvas, (950, -650), 80, 260, 32, 72, 10, 2, lambda nb_points: cycle(smooth_color_generator(colors_pastel2, int(nb_points/2))))
        if spiro_should_turn:
            canvas.rotations[s1] = 0
            canvas.rotations[s2] = 0
            while True:
                canvas.rotations[s1] += 0.005
                canvas.rotations[s2] += 0.003
                canvas.draw_once()
                sleep(0.2)
                if page.current_view_name != "home_page":
                    return
    
    def animate_spiro_show():
        nonlocal canvas_container
        sleep(8)
        n_steps = 1000
        for step in range(n_steps):
            t = step / n_steps
            canvas_container.opacity = ease_in_sine(t)
            if page.current_view_name == "home_page":
                home_page_view.update()
            else:
                return
            sleep(0.005)

    page.run_thread(animation_color)
    page.run_thread(animate_title_position)
    page.run_thread(animate_spiro_background)
    page.run_thread(animate_spiro_show)
    
    return home_page_view

