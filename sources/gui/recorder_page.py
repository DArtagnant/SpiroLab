import flet as ft
from audio.getter import input_sound_start, input_sound_end
from flet_audio_recorder import AudioRecorderStateChangeEvent, AudioRecorderState, AudioRecorder, AudioEncoder
import os

def recorder_page(page: ft.Page, switch_to_showroom_page, switch_to_custom_spiro_page):
    page.current_view_name = "recorder"
    recorder_view = ft.View(
        route="/enregistrer",
        controls= [
            ft.Column([
                info := ft.Text("Enregistrez un audio ou choisissez un fichier pour générer les spirographes à partir de celui-ci.\n(Pensez à activer votre microphone)",
                            text_align=ft.TextAlign.CENTER,
                            size=18),
                ft.Row([
                    input_button := ft.ElevatedButton("Enregistrer", icon=ft.Icons.RADIO_BUTTON_UNCHECKED),
                    file_input := ft.ElevatedButton("Importer un audio .wav", icon=ft.Icons.UPLOAD_FILE),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Text(),
                ft.Text("Vous pouvez aussi construire votre propre spirographe en ajustant à la main les paramètres :",
                        size=18),
                ft.ElevatedButton("Construire un spirographe", on_click=switch_to_custom_spiro_page, icon=ft.Icons.BRUSH),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
            )
        ]
    )

    audio_path = None

    # Enregistement du son
    audio_rec = AudioRecorder(
        audio_encoder=AudioEncoder.WAV,
    )

    page.overlay.append(audio_rec)

    def execute_animation_from_audio():
        nonlocal audio_path
        if audio_path and os.path.exists(audio_path):
            dialog_before_anim = ft.AlertDialog(
                modal=True,
                title=ft.Text("Animation prête"),
                content=ft.Text("Votre audio est bien récupéré.\nMettez votre ambiance musicale puis lancez l'animation."),
                actions_alignment=ft.MainAxisAlignment.END,
                actions=[
                    ft.TextButton("Démarrer", on_click=lambda _: switch_to_showroom_page(None, audio_path))
                ]
            )
            page.open(dialog_before_anim)
        else:
            audio_path = None
            dialog = ft.AlertDialog(
                title=ft.Text("Fichier non-trouvé"),
            )
            page.open(dialog)


    def on_sound_start(_):
        nonlocal input_button, info
        input_sound_start(audio_rec)
        info.value = "Enregistrement en cours."
        input_button.text = "Stop"
        input_button.on_click = on_sound_end
        input_button.icon = ft.Icons.STOP_CIRCLE
        page.update()

    def on_sound_end(_):
        nonlocal input_button, info, audio_path
        audio_path = input_sound_end(audio_rec)
        execute_animation_from_audio()
    
    input_button.on_click = on_sound_start

    def import_audio(e: ft.FilePickerResultEvent):
        nonlocal audio_path
        if e.files:
            audio_path = e.files[0].path
            execute_animation_from_audio()

    import_audio_dialog = ft.FilePicker(on_result=import_audio)
    page.overlay.append(import_audio_dialog)

    file_input.on_click = lambda _: import_audio_dialog.pick_files(
        allow_multiple=False,
        dialog_title="Choisir un fichier audio WAV",
        allowed_extensions=["wav"],
        file_type=ft.FilePickerFileType.CUSTOM,
        initial_directory=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data")), #TODO
    )
    
    return recorder_view

