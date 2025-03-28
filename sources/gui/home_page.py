#Projet : SpiroLab
#Auteurs : Lamiss Elhbishy, Thomas Diot, Pierre Gallois, Jules Charlier, Jim Garnier

import flet as ft
from time import sleep
from .components.centered_canvas import centered_canvas
from .components.spirograph import render_spirograph
from formule.easing import *
from formule.colors_creator import smooth_color_generator
from itertools import cycle

# Texte du logo affiché sur la page d'accueil
LOGO = """
███████╗██████╗ ██╗██████╗  ██████╗ ██╗      █████╗ ██████╗ 
██╔════╝██╔══██╗██║██╔══██╗██╔═══██╗██║     ██╔══██╗██╔══██╗
███████╗██████╔╝██║██████╔╝██║   ██║██║     ███████║██████╔╝
╚════██║██╔═══╝ ██║██╔══██╗██║   ██║██║     ██╔══██║██╔══██╗
███████║██║     ██║██║  ██║╚██████╔╝███████╗██║  ██║██████╔╝
╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═════╝ 
"""

def home_page(page: ft.Page, go_to_view_record, spiro_should_turn: bool = False) -> ft.View:
    """
    Crée la vue d'accueil de l'application, avec des animations et un logo dynamique.
    Cette page présente également un bouton permettant de commencer l'enregistrement d'un audio.

    Args:
        page (ft.Page): L'objet page de l'interface graphique.
        go_to_view_record (function): Fonction permettant de passer à la page d'enregistrement.
        spiro_should_turn (bool): Détermine si les spirographes doivent tourner en arrière-plan.

    Returns:
        ft.View: La vue d'accueil avec son animation et ses contrôles.
    """
    page.current_view_name = "home_page"  # Définir la vue actuelle comme "home_page"
    
    # Création du texte du logo avec un dégradé dynamique
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

    # Création de la vue de la page d'accueil
    home_page_view = ft.View(
        route= "/home",
        controls=[ft.Row([
                    ft.Stack([
                        canvas_container := ft.Container(
                            canvas := centered_canvas(page),  # Création du canevas centré pour le spirographe
                            opacity=0,  # Initialisation de l'opacité à 0 pour l'animation
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
                                opacity=0  # Initialisation de l'opacité à 0 pour l'animation
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

    # Ajout du bouton flottant pour démarrer l'enregistrement
    home_page_view.floating_action_button = ft.FloatingActionButton(text="Commencer", icon=ft.Icons.ARROW_FORWARD, on_click=go_to_view_record, opacity=0)
    home_page_view.floating_action_button_location = ft.FloatingActionButtonLocation.END_FLOAT

    # Fonction pour animer le dégradé du logo
    def animation_color():
        """
        Anime les couleurs du dégradé du logo pour qu'elles changent de manière fluide.
        Cette animation fonctionne en boucle, modifiant les color stops du dégradé.
        Les couleurs changent progressivement à chaque cycle.

        Chaque changement de couleur dure environ 1 seconde avant de recommencer.
        """
        nonlocal paint_color
        colors = [ft.Colors.BLUE, ft.Colors.LIGHT_BLUE, ft.Colors.LIGHT_GREEN, ft.Colors.GREEN, ft.Colors.ORANGE, ft.Colors.RED, ft.Colors.PINK, ft.Colors.DEEP_PURPLE]
        while True:
            # Mise à jour des color stops du dégradé pour créer un effet de changement fluide
            paint_color.color_stops = list(e+0.01 for e in paint_color.color_stops)
            if paint_color.color_stops[-1] > 1:
                # Lorsque la dernière couleur atteint sa limite, on la remet au début
                val = paint_color.color_stops[-1]
                del paint_color.color_stops[-1]
                del paint_color.colors[-1]
                paint_color.color_stops.insert(0, val - 1)
                paint_color.colors.insert(0, colors[(colors.index(paint_color.colors[0]) + 1) % len(colors)])  # Rotation des couleurs
            if page.current_view_name == "home_page":
                home_page_view.update()  # Mise à jour de la vue
            else:
                return  # Si la vue n'est plus "home_page", on arrête l'animation
            sleep(0.1)  # Attendre avant de redessiner le dégradé

    # Fonction pour animer la position du texte d'introduction et du bas de la page
    def animate_title_position():
        """
        Anime l'apparition du texte de bienvenue et de la description de la page d'accueil.
        L'animation fait apparaître progressivement le texte et la description.

        Le bouton flottant devient visible et le texte de bienvenue s'estompe progressivement.
        """
        nonlocal bas, text_bienvenue, page
        sleep(2)  # Temps d'attente avant le début de l'animation
        start_height = 0
        end_height = 400
        total_height = end_height - start_height
        start_opacity = 1
        n_steps = 1000
        for step in range(n_steps):
            t = step / n_steps
            bas.height = start_height + ease_in_out_cubic(t) * total_height  # Animation de la hauteur de la description
            bas.opacity = ease_out_sine(t**3)  # Animation de l'opacité de la description
            home_page_view.floating_action_button.opacity = ease_in_sine(t)  # Animation de l'opacité du bouton
            text_bienvenue.opacity = start_opacity - min(1, ease_in_sine(t*2))  # Animation de l'opacité du texte de bienvenue
            if page.current_view_name == "home_page":
                home_page_view.update()  # Mise à jour de la page à chaque étape de l'animation
            else:
                return  # Si la vue n'est plus "home_page", on arrête l'animation
            sleep(0.005)

    # Fonction pour animer les spirographes en arrière-plan
    def animate_spiro_background():
        """
        Anime deux spirographes en arrière-plan avec des couleurs pastel.
        Si l'option `spiro_should_turn` est activée, les spirographes tourneront.

        L'animation des spirographes commence après un délai, et les spirographes peuvent tourner en boucle.
        """
        nonlocal canvas
        sleep(8)  # Attendre avant de commencer à dessiner les spirographes
        colors_pastel1 = ("#76BA71", "#EDE687", "#F7B05E", "#E67A73", "#99408A")
        colors_pastel2 = ("#8E3600", "#D05903", "#F56517", "#FDAB04", "#EEC5A2", "#492E0B")
        # Créer deux spirographes avec des couleurs différentes
        s1 = render_spirograph(canvas, (-200, 0), 150, 200, 60, 132, 10, 2, lambda nb_points: cycle(smooth_color_generator(colors_pastel1, int(nb_points/2), easing=ease_in_out_cubic)))
        s2 = render_spirograph(canvas, (950, -650), 80, 260, 32, 72, 10, 2, lambda nb_points: cycle(smooth_color_generator(colors_pastel2, int(nb_points/2))))
        # Si on décide de faire tourner les spiros d'arrière plan (demande une puissance non négligeable)
        if spiro_should_turn:
            canvas.rotations[s1] = 0  # Initialisation de la rotation pour le premier spirographe
            canvas.rotations[s2] = 0  # Initialisation de la rotation pour le deuxième spirographe
            while True:
                canvas.rotations[s1] += 0.005  # Rotation du premier spirographe
                canvas.rotations[s2] += 0.003  # Rotation du deuxième spirographe
                canvas.draw_once()  # Redessiner le canevas avec les nouvelles positions
                sleep(0.2)  # Attendre avant de redessiner
                if page.current_view_name != "home_page":
                    return  # Arrêter si la vue n'est plus "home_page"

    # Fonction pour animer l'apparition du canevas
    def animate_spiro_show():
        """
        Anime l'apparition du canevas contenant les spirographes avec un effet d'opacité.
        Le canevas devient progressivement visible avec une animation d'opacité.
        """
        nonlocal canvas_container
        sleep(8)  # Attendre avant de commencer l'animation
        n_steps = 1000
        for step in range(n_steps):
            t = step / n_steps
            canvas_container.opacity = ease_in_sine(t)  # Animation de l'opacité du canevas
            if page.current_view_name == "home_page":
                home_page_view.update()  # Mise à jour de la vue
            else:
                return  # Si la vue n'est plus "home_page", arrêter l'animation
            sleep(0.005)

    # Lancer les threads d'animation en parallèle
    page.run_thread(animation_color)
    page.run_thread(animate_title_position)
    page.run_thread(animate_spiro_background)
    page.run_thread(animate_spiro_show)
    
    return home_page_view
