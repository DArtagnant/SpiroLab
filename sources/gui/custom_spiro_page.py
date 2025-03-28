#Projet : SpiroLab
#Auteurs : Lamiss Elhbishy, Thomas Diot, Pierre Gallois, Jules Charlier, Jim Garnier

import flet as ft
from .components.centered_canvas import centered_canvas
from .components.spirograph import render_spirograph
from math import pi
from formule import svg_creator
from formule.colors_creator import gen_random_color_scheme

def custom_spiro_page(page: ft.Page, switch_to_record):
    """
    Crée une page de personnalisation pour le spirographe où l'utilisateur peut ajuster différents paramètres
    comme les rayons, la fréquence, la couleur et la rotation du spirographe.
    
    Args:
        page (ft.Page): La page Flet sur laquelle la vue de personnalisation sera rendue.
        switch_to_record (function): Fonction permettant de revenir à l'écran d'enregistrement.
    
    Returns:
        ft.View: La vue de personnalisation contenant le canevas et les contrôles de paramètres.
    """
    page.current_view_name = "custom_spiro"  # Définition du nom de la vue pour la page actuelle
    cc = centered_canvas(page)  # Création d'un canevas centré où le spirographe sera dessiné

    # Définition de la vue de la page avec des contrôles pour la personnalisation du spirographe
    custom_spiro_page_view = ft.View(
        route="personalisation",  # Route de la page (pour la navigation)
        controls=[
            ft.Row([  # Disposition horizontale pour le canevas et les contrôles
                ft.Container(
                    cc,  # Le canevas est ajouté ici
                    expand=True,  # Le canevas occupe tout l'espace disponible
                ),
                ft.Column([  # Colonne verticale pour les contrôles
                    ft.Text("Paramètres :", theme_style=ft.TextThemeStyle.HEADLINE_SMALL),
                    ft.Text("Rayon du grand cercle"),
                    large_radius := ft.Slider(label="{value}px", min=10, max=300, value=100),  # Slider pour ajuster le rayon du grand cercle
                    ft.Text("Rayon du petit cercle"),
                    small_radius := ft.Slider(label="{value}px", min=10, max=300, value=30),  # Slider pour ajuster le rayon du petit cercle
                    ft.Text("Fréquence du petit cercle"),
                    large_frequency := ft.Slider(label="{value}", min=5, max=100, divisions=95, value=25),  # Slider pour la fréquence du grand cercle
                    ft.Text("Fréquence du point"),
                    small_frequency := ft.Slider(label="{value}", min=5, max=100, divisions=95, value=50),  # Slider pour la fréquence du point
                    ft.Text("Tourner"),
                    turn := ft.Slider(label="{value}", min=0, max=2*pi, value=0),  # Slider pour la rotation du spirographe
                    ft.Text("Couleur"),
                    color := ft.Slider(label="{value}", min=0, max=10, divisions=10, value=0),  # Slider pour la couleur du spirographe
                    export := ft.ElevatedButton("Exporter en svg", icon=ft.Icons.DOWNLOAD),  # Bouton pour exporter en SVG
                    ft.Text(""),
                    ft.ElevatedButton("Retour à l'enregistrement", on_click=switch_to_record, icon=ft.Icons.ARROW_BACK),  # Bouton pour revenir à la page d'enregistrement
                ],
                width=300)  # La colonne des contrôles a une largeur fixe de 300px
            ],
            expand=True)  # Le Row prend tout l'espace disponible
        ]
    )

    def recompute_spirograph(_):
        """
        Recalcule et redessine le spirographe avec les valeurs actuelles des sliders. 
        Cette fonction est appelée chaque fois qu'un slider change de valeur.
        
        Args:
            _: Argument ignoré, nécessaire pour la signature de la fonction attachée aux événements `on_change`.
        """
        cc.remove_all()  # On efface tout le contenu du canevas avant de redessiner
        # Création du spirographe avec les valeurs des sliders
        spiro_id = render_spirograph(
            cc,
            (0, 0),  # Position de départ du spirographe
            float(large_radius.value),  # Rayon du grand cercle
            float(small_radius.value),  # Rayon du petit cercle
            int(large_frequency.value),  # Fréquence du grand cercle
            int(small_frequency.value),  # Fréquence du petit cercle
            40,  # Nombre d'itérations pour le dessin
            iter_color=gen_random_color_scheme(int(color.value))  # Génération d'une couleur aléatoire en fonction du slider
        )
        # Applique une rotation au spirographe basé sur la valeur du slider de rotation
        cc.rotations[spiro_id] = float(turn.value)
        cc.draw_once()  # Dessine le spirographe sur le canevas une fois recalculé

    # Attache la fonction recompute_spirograph à tous les sliders, ainsi le spirographe est mis à jour en temps réel
    large_radius.on_change = recompute_spirograph
    small_radius.on_change = recompute_spirograph
    large_frequency.on_change = recompute_spirograph
    small_frequency.on_change = recompute_spirograph
    turn.on_change = recompute_spirograph
    color.on_change = recompute_spirograph

    def save_spiro(e: ft.FilePickerResultEvent):
        """
        Sauvegarde le spirographe sous forme de fichier SVG dans le dossier choisi par l'utilisateur.
        
        Args:
            e (ft.FilePickerResultEvent): Événement contenant le chemin du dossier où le fichier sera sauvegardé.
        """
        if e.path:
            # Création du fichier SVG avec les paramètres actuels du spirographe
            svg_creator.create_svg_for(
                tuple(cc.spiros.values())[0],  # Récupère le spirographe
                tuple(cc.centers.values())[0],  # Récupère le centre du spirographe
                e.path + "/spiro.svg",  # Le chemin du fichier à sauvegarder
                20,  # Résolution du SVG
                tuple(cc.rotations.values())[0]  # Rotation actuelle du spirographe
            )
    
    # Création d'un dialogue pour choisir le dossier de sauvegarde
    save_spiro_dialog = ft.FilePicker(on_result=save_spiro)
    page.overlay.append(save_spiro_dialog)  # Ajoute le dialogue à la superposition de la page

    # Lorsque l'utilisateur clique sur le bouton "Exporter en svg", on affiche le dialogue pour choisir le dossier de sauvegarde
    export.on_click = lambda _: save_spiro_dialog.get_directory_path(dialog_title="Choisir un dossier, le fichier sera sauvé sous le nom de spiro.svg")

    # On appelle une première fois recompute_spirograph pour afficher le spirographe avec les valeurs par défaut
    recompute_spirograph(None)
    
    # Retourne la vue de la page personnalisée
    return custom_spiro_page_view
