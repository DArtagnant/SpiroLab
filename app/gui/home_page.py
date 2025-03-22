import flet as ft
from time import sleep

LOGO ="""
███████╗██████╗ ██╗██████╗  ██████╗ ██╗      █████╗ ██████╗ 
██╔════╝██╔══██╗██║██╔══██╗██╔═══██╗██║     ██╔══██╗██╔══██╗
███████╗██████╔╝██║██████╔╝██║   ██║██║     ███████║██████╔╝
╚════██║██╔═══╝ ██║██╔══██╗██║   ██║██║     ██╔══██║██╔══██╗
███████║██║     ██║██║  ██║╚██████╔╝███████╗██║  ██║██████╔╝
╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═════╝ 
"""


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
        ]
    )

    page.add(ft.Row([
        ft.Column([
            logo_text,
            ft.Text("Bienvenue dans SpiroLab !", size=18),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        ],
        alignment= ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
    ))

    def animation():
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

    page.run_thread(animation)
    

"""ft.PaintLinearGradient(
                            tuple(e*10 for e in range(8)),
                            tuple(80 + e*10 for e in range(8)),
                            [ft.Colors.BLUE, ft.Colors.LIGHT_BLUE, ft.Colors.LIGHT_GREEN, ft.Colors.GREEN, ft.Colors.ORANGE, ft.Colors.RED, ft.Colors.PINK, ft.Colors.DEEP_PURPLE]
                        ))"""