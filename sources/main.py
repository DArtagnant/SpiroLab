#!/usr/bin/python3
import flet as ft
import os
import sys

# TODO
if os.getenv("FLET_APP_STORAGE_TEMP") is None:
    print("! L'application doit être lancée depuis le dossier sources à l'aide de la commande 'flet run'")
    print("! Nous essayons de lancer tout de même l'application")
    # Essayons de lancer l'app tout de même
    main_py_path = os.path.dirname(os.path.abspath(__file__))
    os.system(f"flet run {main_py_path}")
    sys.exit()

from gui.render import main

ft.app(target=main, assets_dir="assets")