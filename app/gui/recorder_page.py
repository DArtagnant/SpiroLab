import flet as ft
from audio.getter import input_sound_start, input_sound_end

def recorder_page(page: ft.Page, switch_to_showroom_page):
    recorder_view = ft.View(
        route="/enregistrer",
        controls= [
            ft.Column([
                info := ft.Text("Enregistrez un audio ou choisissez un fichier pour générer les spirographes à partir de celui-ci.\n(Pensez à activer votre microphone)", text_align=ft.TextAlign.CENTER),
                ft.Row([
                    input_button := ft.ElevatedButton("Enregistrer"),
                    file_input := ft.ElevatedButton("Importer un audio .wav"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
            )
        ]
    )

    audio_path = None

    def execute_animation_from_audio():
        nonlocal audio_path
        switch_to_showroom_page(None, audio_path)


    def on_sound_start(_):
        nonlocal input_button, info
        input_sound_start(None)
        info.value = "Enregistrement en cours."
        input_button.text = "Stop"
        input_button.on_click = on_sound_end

    def on_sound_end(_):
        nonlocal input_button, info, audio_path
        audio_path = input_sound_end(None)
        execute_animation_from_audio()
    
    input_button.on_click = on_sound_start

    def import_audio(e: ft.FilePickerResultEvent):
        nonlocal audio_path
        if e.files:
            audio_path = e.files[0].path
            execute_animation_from_audio()

    import_audio_dialog = ft.FilePicker(on_result=import_audio)
    page.overlay.append(import_audio_dialog)

    file_input.on_click = lambda _: import_audio_dialog.pick_files(allow_multiple=False, dialog_title="Choisir un fichier audio WAV", allowed_extensions=["wav"], file_type=ft.FilePickerFileType.CUSTOM)
    
    return recorder_view

