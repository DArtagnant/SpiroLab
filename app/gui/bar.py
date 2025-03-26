import flet as ft
from .spirograph import render_spirograph

from audio.getter import input_sound_start, input_sound_end, read_wav, audio_rec, input_path
from time import sleep
from random import randint
from formule import create_svg_for, colors_creator
from flet.core.protocol import Command
from formule.normalization import normalize_around

MAX_SPIROS_ON_SCREEN = 4


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

    def compute_spirographs_from_wav(path):
        # TODO : empêcher cette fonction de continuer à s'éxécuter quand on commence à faire autre chose, type afficher un autre spiro
        arrays = read_wav(path)

        large_radii = normalize_around(arrays[0], 70, 60)
        small_radii = normalize_around(arrays[1], 60, 50)
        large_frequencies = normalize_around(arrays[2], 45, 40).astype(int) # On s'assure de n'avoir que des entiers dans la liste
        small_frequencies = normalize_around(arrays[3], 35, 30).astype(int)
        resolution = normalize_around(arrays[4], 35, 15) # TODO : vérifier que ces valeurs ne sont pas débiles

        current_nb_spiros = 0
        for i in range(len(large_radii)):
            # Si le spirographe affiché n'est pas suffisemment différent du dernier, on passe
            # Permet de ne jamais avoir deux spirographes presque identiques d'affilée
            if (i != 0 and
                abs(large_frequencies[i] - large_frequencies[i-1]) <= 4 and
                abs(small_frequencies[i] - small_frequencies[i-1]) <= 4
            ):
                continue

            if current_nb_spiros%MAX_SPIROS_ON_SCREEN == 0:
                canvas.remove_all()

            render_spirograph(
                canvas,
                (randint(-500, 500), randint(-200, 200)), # Position aléatoire

                large_radii[i],
                small_radii[i],
                int(large_frequencies[i]),
                int(small_frequencies[i]),
                resolution[i],

                iter_color = colors_creator.gen_random_color_scheme()
            )

            sleep(0.5)
            canvas.draw_once()
            current_nb_spiros = (current_nb_spiros + 1)%MAX_SPIROS_ON_SCREEN
        
    large_radius = ft.TextField(label="Rayon du grand cercle", value='125')
    small_radius = ft.TextField(label="Rayon du petit cercle", value='200')

    large_frequency = ft.TextField(label="Fréquence du petit cercle", value='75')
    small_frequency = ft.TextField(label="Fréquence du point", value='50')

    resolution = ft.TextField(label="Resolution", value='50')

    b = ft.ElevatedButton(text="Afficher", on_click=recompute_spirograph)

    page.overlay.append(audio_rec)

    input_button = ft.ElevatedButton(text="Enregistrer", on_click=input_sound_start)
    # stop_input_button = ft.ElevatedButton(text="Stop", on_click=lambda _: page._Page__conn.send_command(page._session_id, Command(0, 'clean', [canvas.uid], {})))
    stop_input_button = ft.ElevatedButton(text="Stop", on_click=input_sound_end)

    # TODO : Mettre le bon path -> voir le dossier temp dans getter.py ?
    def export_spiro(_):
        spiro_id = tuple(canvas.spiros.keys())[-1]
        # create_svg_for(canvas.spiros[spiro_id], canvas.centers[spiro_id], "/home/thomas/Programmation/projet-NSI/a.svg", angle=canvas.rotations.get(spiro_id, None))

    export_button = ft.ElevatedButton(text="Exporter un spirographe", on_click=export_spiro)

    def import_audio(e: ft.FilePickerResultEvent):
        if e.files:
            file = e.files[0].path
            compute_spirographs_from_wav(file)

    import_audio_dialog = ft.FilePicker(on_result=import_audio)
    page.overlay.append(import_audio_dialog)

    import_audio_button = ft.ElevatedButton(text="Importer un audio", on_click=lambda _: import_audio_dialog.pick_files(allow_multiple=False, dialog_title="Choisir un fichier audio WAV", allowed_extensions=["wav"], file_type=ft.FilePickerFileType.CUSTOM))

    # Automatisation de la génération du spirographe à chaque pression de la touche 'Enter'
    def on_keyboard(e: ft.KeyboardEvent):
        if e.key == 'R':
            canvas.remove_all()
            compute_spirographs_from_wav(input_path) # TODO : faire un bouton pour afficher les spiros de l'enregistrement
        if e.key == 'Enter':
            canvas.remove_all()
            recompute_spirograph("_")


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