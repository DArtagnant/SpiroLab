#Projet : SpiroLab
#Auteurs : Lamiss Elhbishy, Thomas Diot, Pierre Gallois, Jules Charlier, Jim Garnier

import flet as ft
from .components.centered_canvas import centered_canvas
from audio.getter import read_wav
from formule.normalization import normalize_around
from random import randint
from formule import colors_creator
from .components.spirograph import render_spirograph
from time import sleep
from formule import easing

MAX_SPIROS_ON_SCREEN = 4  # Nombre maximal de spirographes affichés à l'écran en même temps
MARGE = 50  # Marge autour de l'écran pour éviter que les spirographes ne sortent trop du cadre

def compute_spirographs_from_wav(page: ft.Page, canvases: list, containers: list, path: str):
    """
    Fonction principale pour générer des spirographes à partir des données extraites d'un fichier WAV.
    Elle lit les données audio, les normalise, puis génère et anime les spirographes à l'écran.

    Args:
        page (ft.Page): L'objet page de l'interface graphique.
        canvases (list): Liste des canvases (sur lesquels les spirographes seront dessinés).
        containers (list): Liste des containers associés aux canvases, permettant de gérer l'opacité des éléments.
        path (str): Le chemin vers le fichier audio WAV à utiliser.
    """
    arrays = read_wav(path)

    # Normalisation des paramètres des spirographes à partir des données audio
    large_radii = normalize_around(arrays[0], 70, 60)
    small_radii = normalize_around(arrays[1], 60, 50)
    large_frequencies = normalize_around(arrays[2], 45, 40).astype(int)  # Assure que les fréquences sont des entiers
    small_frequencies = normalize_around(arrays[3], 35, 30).astype(int)
    resolution = normalize_around(arrays[4], 60, 15)

    current_nb_spiros = 0  # Nombre actuel de spirographes à l'écran
    j = 0  # Index pour gérer les canvases et containers

    for i in range(len(large_radii)):
        # Si l'utilisateur a changé de vue (par exemple, navigué ailleurs), on arrête la fonction.
        if page.current_view_name != "showroom":
            return
        
        # On vérifie que le spirographe actuel est suffisamment différent du précédent pour éviter les répétitions
        if (i != 0 and
            abs(large_frequencies[i] - large_frequencies[i - 1]) <= 4 and
            abs(small_frequencies[i] - small_frequencies[i - 1]) <= 4
        ):
            continue

        # Attente que la taille de la page soit définie pour éviter des erreurs de positionnement
        while page.width is None or page.height is None:
            print("double skipped frame")
            page.update()
            sleep(0.01)

        # Sélectionne les canvases et containers en fonction de l'index
        before = j % len(canvases)
        now = (j + 1) % len(canvases)
        
        # Génération du spirographe avec les paramètres correspondants
        render_spirograph(
            canvases[before],
            (randint(MARGE, int(page.width) - MARGE), randint(int(-page.height) + MARGE, -MARGE)),  # Position aléatoire du spirographe
            large_radii[i],
            small_radii[i],
            int(large_frequencies[i]),
            int(small_frequencies[i]),
            resolution[i],
            iter_color=colors_creator.gen_random_color_scheme()  # Génère une palette de couleurs aléatoire
        )

        canvases[before].draw_once()
        
        # Animation entre les containers, changement progressif de l'opacité pour une transition fluide
        n_steps = 250  # Nombre de pas pour l'animation
        for step in range(n_steps):
            t = step / n_steps
            containers[before].opacity = easing.ease_in_sine(t)
            containers[now].opacity = 1 - easing.ease_out_sine(t)
            page.update()
            sleep(0.01)

        # Réinitialisation de l'opacité pour la prochaine itération
        containers[before].opacity = 1
        canvases[now].remove_all()
        page.update()

        # Mise à jour du nombre de spirographes affichés à l'écran
        current_nb_spiros = (current_nb_spiros + 1) % MAX_SPIROS_ON_SCREEN
        j += 1

def showroom_page(page: ft.Page, audio_path: str, custom_spiro) -> ft.View:
    """
    Crée la vue principale de l'interface, affichant des spirographes animés à partir d'un fichier audio.

    Args:
        page (ft.Page): L'objet page de l'interface graphique.
        audio_path (str): Le chemin vers le fichier audio WAV à utiliser pour générer les spirographes.
        custom_spiro (function): Fonction permettant à l'utilisateur de créer son propre spirographe.

    Returns:
        ft.View: La vue du showroom avec les spirographes animés.
    """
    # Nom de la vue actuelle (utile pour la gestion de la navigation entre les pages)
    page.current_view_name = "showroom"

    # Création des canvases centrés pour afficher les spirographes
    cc1 = centered_canvas(page)
    cc2 = centered_canvas(page)
    cc3 = centered_canvas(page)

    # Vue principale avec les trois canvases
    showroom_page_view = ft.View(
        route="/dessin",  # Route de navigation pour la page de dessin
        controls=[
            ft.Stack([
                ccc1 := ft.Container(cc1, expand=True),
                ccc2 := ft.Container(cc2, expand=True),
                ccc3 := ft.Container(cc3, expand=True),
            ], expand=True)
        ],
    )

    # Bouton flottant pour permettre à l'utilisateur de créer son propre spirographe
    showroom_page_view.floating_action_button = ft.FloatingActionButton(
        text="Construire son propre spirographe", icon=ft.Icons.BRUSH, on_click=custom_spiro
    )

    # Lancement du calcul des spirographes dans un thread séparé pour ne pas bloquer l'interface
    page.run_thread(lambda: compute_spirographs_from_wav(page, [cc1, cc2, cc3], [ccc1, ccc2, ccc3], audio_path))

    return showroom_page_view
