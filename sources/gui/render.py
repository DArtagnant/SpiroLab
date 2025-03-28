# Projet : SpiroLab
# Auteurs : Lamiss Elhbishy, Thomas Diot, Pierre Gallois, Jules Charlier, Jim Garnier

import flet as ft

# Importation des pages spécifiques utilisées dans l'application
from .home_page import home_page
from .recorder_page import recorder_page
from .showroom_page import showroom_page
from .custom_spiro_page import custom_spiro_page

def main(page: ft.Page):
    """
    Fonction principale qui est appelée au démarrage de l'application.
    
    Elle définit les pages de l'application et gère les transitions entre elles.
    
    Paramètres :
        - page (ft.Page) : La page de l'application gérée par Flet.
    """
    page.title = "SpiroLab"  # Définit le titre de la page

    # Définition de la police de caractères monospace qui est utilisée pour le titre dans l'application
    page.fonts = {
        "monospace": "Monospace.ttf"
    }

    # Fonction pour changer vers la page de l'enregistreur
    def switch_to_recorder(_):
        """
        Change la vue actuelle vers la page d'enregistrement.
        
        Cela efface toutes les vues de la page actuelle, puis ajoute la vue de l'enregistrement.
        
        Paramètres :
            - _ : Un paramètre inutilisé (souvent utilisé pour des fonctions de rappel).
        """
        page.views.clear()  # Efface toutes les vues actuellement affichées
        # Ajoute la vue de l'enregistreur, avec des callbacks pour naviguer vers d'autres pages
        page.views.append(recorder_page(page, switch_to_showroom_page, switch_to_custom_spiro_page))
        page.update()  # Met à jour l'interface de la page pour appliquer les changements

    # Fonction pour changer vers la page d'accueil
    def switch_to_home_page(_):
        """
        Change la vue actuelle vers la page d'accueil.
        
        Cela efface toutes les vues de la page actuelle, puis ajoute la vue d'accueil.
        
        Paramètres :
            - _ : Un paramètre inutilisé (souvent utilisé pour des fonctions de rappel).
        """
        page.views.clear()  # Efface toutes les vues actuellement affichées
        # Ajoute la vue d'accueil, avec un callback pour passer à la page d'enregistrement
        page.views.append(home_page(page, go_to_view_record=switch_to_recorder))
        page.update()  # Met à jour l'interface de la page pour appliquer les changements

    # Fonction pour changer vers la page showroom avec le chemin vers l'audio
    def switch_to_showroom_page(_, audio_path):
        """
        Change la vue actuelle vers la page showroom en fournissant un chemin audio.
        
        Paramètres :
            - _ : Un paramètre inutilisé (souvent utilisé pour des fonctions de rappel).
            - audio_path (str) : Le chemin vers le fichier audio à afficher dans la page showroom.
        """
        page.views.clear()  # Efface toutes les vues actuellement affichées
        # Ajoute la vue showroom avec le chemin de l'audio et le callback pour la page personnalisée
        page.views.append(showroom_page(page, audio_path, switch_to_custom_spiro_page))
        page.update()  # Met à jour l'interface de la page pour appliquer les changements

    # Fonction pour changer vers la page personnalisée Spiro
    def switch_to_custom_spiro_page(_):
        """
        Change la vue actuelle vers la page de spiro personnalisée.
        
        Paramètres :
            - _ : Un paramètre inutilisé (souvent utilisé pour des fonctions de rappel).
        """
        page.views.clear()  # Efface toutes les vues actuellement affichées
        # Ajoute la vue personnalisée Spiro, avec un callback pour la page d'enregistrement
        page.views.append(custom_spiro_page(page, switch_to_recorder))
        page.update()  # Met à jour l'interface de la page pour appliquer les changements

    # Initialisation de l'application en chargeant la page d'accueil
    switch_to_home_page(None)
