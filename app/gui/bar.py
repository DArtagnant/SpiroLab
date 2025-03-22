import flet as ft
from .spirograph import render_spirograph
from audio.getter import input_sound_start, input_sound_end, read_wav, audio_rec
from time import sleep
from numpy import real, imag
from random import randint
from formule import create_svg_for
from flet.core.protocol import Command

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
        
    large_radius = ft.TextField(label="Rayon du grand cercle", value='125')
    small_radius = ft.TextField(label="Rayon du petit cercle", value='200')

    large_frequency = ft.TextField(label="Fréquence du petit cercle", value='100')
    small_frequency = ft.TextField(label="Fréquence du point", value='50')

    resolution = ft.TextField(label="Resolution", value='50')

    b = ft.ElevatedButton(text="Afficher", on_click=recompute_spirograph)

    page.overlay.append(audio_rec)

    input_button = ft.ElevatedButton(text="Enregistrer", on_click=input_sound_start)
    stop_input_button = ft.ElevatedButton(text="Stop", on_click=lambda _: page._Page__conn.send_command(page._session_id, Command(0, 'clean', [canvas.uid], {})))

    # Automatisation de la génération du spirographe à chaque pression de la touche 'Enter'
    def on_keyboard(e: ft.KeyboardEvent):
        if e.key == 'R':
            recompute_spirograph_from_wav()
        if e.key == 'M':
            recompute_spirograph("") # Affiche le spirographe par défaut


    page.on_keyboard_event = on_keyboard

    def next_turn(_):
        large_radius.value = float(large_radius.value) + 5
        resolution.value = float(resolution.value) + 5

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

    next_turn_button = ft.ElevatedButton(
        text="next turn",
        on_click=next_turn,
    )

    

    # clean : page._Page__conn.send_command(page._session_id, Command(0, 'clean', [canvas.uid], {}))

    # Exemples :
    """
    add [] {'to': '_17', 'at': '84'} [Command(indent=0, name=None, values=['line'], attrs={'paint': '{"color":"#00fff7","stroke_cap":"round","stroke_join":"round","stroke_width":5}', 'x1': '641.6697576615708', 'x2': '672.2017358014425', 'y1': '578.3384275558999', 'y2': '579.7716054927121'}, commands=[])]
add [] {'to': '_17', 'at': '85'} [Command(indent=0, name=None, values=['line'], attrs={'paint': '{"color":"#00d9ff","stroke_cap":"round","stroke_join":"round","stroke_width":5}', 'x1': '672.2017358014425', 'x2': '703.0102843352246', 'y1': '579.7716054927121', 'y2': '577.7264241133312'}, commands=[])]
add [] {'to': '_17', 'at': '86'} [Command(indent=0, name=None, values=['line'], attrs={'paint': '{"color":"#00abff","stroke_cap":"round","stroke_join":"round","stroke_width":5}', 'x1': '703.0102843352246', 'x2': '733.6791823335403', 'y1': '577.7264241133312', 'y2': '572.1737339267407'}, commands=[])]
add [] {'to': '_17', 'at': '87'} [Command(indent=0, name=None, values=['line'], attrs={'paint': '{"color":"#007eff","stroke_cap":"round","stroke_join":"round","stroke_width":5}', 'x1': '733.6791823335403', 'x2': '763.7904182641198', 'y1': '572.1737339267407', 'y2': '563.1354488643242'}, commands=[])]
add [] {'to': '_17', 'at': '88'} [Command(indent=0, name=None, values=['line'], attrs={'paint': '{"color":"#0050ff","stroke_cap":"round","stroke_join":"round","stroke_width":5}', 'x1': '763.7904182641198', 'x2': '792.9305231718591', 'y1': '563.1354488643242', 'y2': '550.6844597955899'}, commands=[])]
    """


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
        ]),
        ft.Column([
            input_button,
            stop_input_button,
            next_turn_button,
        ])
    ])