import flet as ft
from time import sleep
from math import sin, cos, pi

LOGO ="""
███████╗██████╗ ██╗██████╗  ██████╗ ██╗      █████╗ ██████╗ 
██╔════╝██╔══██╗██║██╔══██╗██╔═══██╗██║     ██╔══██╗██╔══██╗
███████╗██████╔╝██║██████╔╝██║   ██║██║     ███████║██████╔╝
╚════██║██╔═══╝ ██║██╔══██╗██║   ██║██║     ██╔══██║██╔══██╗
███████║██║     ██║██║  ██║╚██████╔╝███████╗██║  ██║██████╔╝
╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═════╝ 
"""

def ease_in_out_cubic(t):
    if t < 0.5:
        return 4 * t**3
    else:
        return 1 - ((-2 * t + 2) ** 3) / 2

def ease_in_cubic(t):
    return t**3

def ease_in_sine(t):
    return 1 - cos((t * pi) / 2)

def ease_out_sine(t):
    return sin((t * pi) / 2)


def home_page(page: ft.Page):

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
                    ft.Column([
                        logo_text,
                        text_bienvenue := ft.Text("Bienvenue dans SpiroLab !", size=18, opacity=1),
                        bas := ft.Container(
                            ft.Text("Lorem Ipsum zkafuea umjd sqfksqjdfkq fehazkfjhqfzjhml zjhkmlafhme hfjza  fjhkzafjh jfhzaljfhzfeajhzekmfjh zekfhjzeaflhzaegf"),
                            height=0,
                            opacity=0
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
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

    page.run_thread(animation_color)
    page.run_thread(animate_title_position)
