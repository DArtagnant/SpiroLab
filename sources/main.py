#!/usr/bin/python3
# Projet : SpiroLab
# Auteurs : Lamiss Elhbishy, Thomas Diot, Pierre Gallois, Jules Charlier, Jim Garnier

import flet as ft  # Importation du module flet pour créer l'application
import os
import sys

# Cette condition permet de vérifier si l'application est lancée depuis le bon environnement
# (en utilisant la commande `flet run` dans le dossier `sources`).
# Si ce n'est pas le cas, un message d'avertissement s'affiche et l'application tente de s'exécuter 
# malgré tout. Cela assure une certaine flexibilité dans l'exécution du code.
if os.getenv("FLET_APP_STORAGE_TEMP") is None:
    print("! L'application doit être lancée depuis le dossier sources à l'aide de la commande 'flet run'")
    print("! Nous essayons de lancer tout de même l'application")
    
    # Récupère le chemin absolu du fichier courant pour s'assurer de son emplacement
    # avant d'essayer de lancer `flet run` avec le bon chemin.
    main_py_path = os.path.dirname(os.path.abspath(__file__))
    
    # Utilise `os.system` pour lancer la commande `flet run` en ligne de commande
    # avec le chemin du fichier actuel comme argument. Cela permet de relancer l'application 
    # dans le bon environnement si elle a été exécutée directement.
    os.system(f"flet run {main_py_path}")
    
    # Quitte le script après avoir lancé la commande ci-dessus.
    # Ceci empêche le code de continuer à s'exécuter après avoir initié la commande.
    sys.exit()

# Importation du module `main` depuis le fichier `gui.render`.
# Ce fichier semble contenir la logique principale de l'interface graphique de l'application.
from gui.render import main

# Lancement de l'application Flet avec la fonction `main` comme point d'entrée
# et le dossier 'assets' spécifié pour les ressources (images, styles, etc.).
ft.app(target=main, assets_dir="assets")
