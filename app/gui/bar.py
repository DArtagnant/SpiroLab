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

    def export_spiro(_):
        spiro_id = tuple(canvas.spiros.keys())[-1]
        create_svg_for(canvas.spiros[spiro_id], canvas.centers[spiro_id], "/home/thomas/Programmation/projet-NSI/a.svg", angle=canvas.rotations.get(spiro_id, None))

    export_button = ft.ElevatedButton(text="Exporter un spirographe", on_click=export_spiro)

    def import_audio(e: ft.FilePickerResultEvent):
        if e.files:
            file = e.files[0]
            print(file)

    import_audio_dialog = ft.FilePicker(on_result=import_audio)
    page.overlay.append(import_audio_dialog)

    import_audio_button = ft.ElevatedButton(text="Importer un audio", on_click=lambda _: import_audio_dialog.pick_files(allow_multiple=False, dialog_title="Choisir un fichier audio WAV", allowed_extensions=["wav"], file_type=ft.FilePickerFileType.CUSTOM))

    # Automatisation de la génération du spirographe à chaque pression de la touche 'Enter'
    def on_keyboard(e: ft.KeyboardEvent):
        if e.key == 'R':
            recompute_spirograph_from_wav()
        if e.key == 'M':
            recompute_spirograph("") # Affiche le spirographe par défaut


    page.on_keyboard_event = on_keyboard

    def next_turn(_):
        spiro_id = tuple(canvas.spiros.keys())[-1]
        canvas.rotations[spiro_id] = canvas.rotations.get(spiro_id, 0) + 0.1
        canvas.clear()
        canvas.draw()
        # large_radius.value = float(large_radius.value) + 5
        # resolution.value = float(resolution.value) + 5

        # canvas.shapes = []
        # render_spirograph(
        #     canvas,
        #     (0,0),
        #     float(large_radius.value),
        #     float(small_radius.value),
        #     int(large_frequency.value),
        #     int(small_frequency.value),
        #     float(resolution.value),
        # )
        # page.update()

    next_turn_button = ft.ElevatedButton(
        text="next turn",
        on_click=next_turn,
    )

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
            export_button,
            import_audio_button,
        ])
    ])