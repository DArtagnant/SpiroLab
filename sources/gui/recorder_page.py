#Projet : SpiroLab
#Auteurs : Lamiss Elhbishy, Thomas Diot, Pierre Gallois, Jules Charlier, Jim Garnier

import flet as ft
from audio.getter import input_sound_start, input_sound_end
from flet_audio_recorder import AudioRecorder, AudioEncoder
import os

def recorder_page(page: ft.Page, switch_to_showroom_page, switch_to_custom_spiro_page):
    """
    Crée la vue d'enregistrement pour l'utilisateur, permettant de soit enregistrer un audio en direct,
    soit importer un fichier audio pour générer des spirographes à partir de celui-ci.

    Args:
        page (ft.Page): L'objet page de l'interface graphique.
        switch_to_showroom_page (function): Fonction permettant de passer à la page du showroom avec l'animation.
        switch_to_custom_spiro_page (function): Fonction permettant de passer à la page où l'utilisateur peut créer son propre spirographe.
    
    Returns:
        ft.View: La vue d'enregistrement pour l'utilisateur.
    """
    page.current_view_name = "recorder"  # Définir la vue actuelle comme "recorder"
    
    # Création de la vue d'enregistrement avec des boutons pour enregistrer ou importer un fichier audio
    recorder_view = ft.View(
        route="/enregistrer",
        controls=[
            ft.Column([
                info := ft.Text(
                    "Enregistrez un audio ou choisissez un fichier pour générer les spirographes à partir de celui-ci.\n(Pensez à activer votre microphone)",
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

    # Variable pour stocker le chemin du fichier audio
    audio_path = None

    # Initialisation du lecteur audio avec l'encodeur WAV
    audio_rec = AudioRecorder(
        audio_encoder=AudioEncoder.WAV,
    )

    # Ajouter l'enregistreur audio en superposition sur la page
    page.overlay.append(audio_rec)

    def execute_animation_from_audio():
        """
        Fonction pour démarrer l'animation des spirographes à partir du fichier audio récupéré.
        Si un fichier audio valide est trouvé, une boîte de dialogue est ouverte pour permettre à l'utilisateur
        de lancer l'animation, sinon, une alerte est affichée.
        """
        nonlocal audio_path
        if audio_path and os.path.exists(audio_path):  # Vérifie si le fichier audio existe
            dialog_before_anim = ft.AlertDialog(
                modal=True,
                title=ft.Text("Animation prête"),
                content=ft.Text("Votre audio est bien récupéré.\nMettez votre ambiance musicale puis lancez l'animation."),
                actions_alignment=ft.MainAxisAlignment.END,
                actions=[
                    ft.TextButton("Démarrer", on_click=lambda _: switch_to_showroom_page(None, audio_path))
                ]
            )
            page.open(dialog_before_anim)  # Ouvre la boîte de dialogue de confirmation
        else:
            audio_path = None
            dialog = ft.AlertDialog(
                title=ft.Text("Fichier non-trouvé"),
            )
            page.open(dialog)  # Ouvre la boîte de dialogue en cas de problème avec le fichier audio

    def on_sound_start(_):
        """
        Cette fonction est appelée lorsque l'enregistrement sonore commence.
        Elle met à jour l'interface pour indiquer que l'enregistrement est en cours et change le bouton pour arrêter l'enregistrement.
        """
        nonlocal input_button, info
        input_sound_start(audio_rec)  # Démarre l'enregistrement audio
        info.value = "Enregistrement en cours."  # Mise à jour du texte de l'information
        input_button.text = "Stop"  # Change le texte du bouton pour "Stop"
        input_button.on_click = on_sound_end  # Configure le bouton pour arrêter l'enregistrement
        input_button.icon = ft.Icons.STOP_CIRCLE  # Change l'icône du bouton en "Stop"
        page.update()

    def on_sound_end(_):
        """
        Cette fonction est appelée lorsque l'enregistrement sonore se termine.
        Elle récupère le chemin du fichier audio enregistré et lance l'animation à partir de ce fichier.
        """
        nonlocal input_button, info, audio_path
        audio_path = input_sound_end(audio_rec)  # Récupère le chemin du fichier audio enregistré
        execute_animation_from_audio()  # Démarre l'animation des spirographes

    input_button.on_click = on_sound_start  # Associe la fonction de démarrage à l'événement du bouton

    def import_audio(e: ft.FilePickerResultEvent):
        """
        Fonction pour importer un fichier audio .wav sélectionné par l'utilisateur.
        Si un fichier est sélectionné, l'animation est lancée avec ce fichier audio.
        """
        nonlocal audio_path
        if e.files:
            audio_path = e.files[0].path  # Récupère le chemin du fichier sélectionné
            execute_animation_from_audio()  # Démarre l'animation des spirographes

    # Initialisation du dialogue pour sélectionner un fichier audio
    import_audio_dialog = ft.FilePicker(on_result=import_audio)
    page.overlay.append(import_audio_dialog)

    # Lorsqu'on clique sur le bouton "Importer un audio", on ouvre le dialogue de sélection de fichier audio
    file_input.on_click = lambda _: import_audio_dialog.pick_files(
        allow_multiple=False,
        dialog_title="Choisir un fichier audio WAV",
        allowed_extensions=["wav"],
        file_type=ft.FilePickerFileType.CUSTOM,
        initial_directory=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data")),
    )

    return recorder_view
