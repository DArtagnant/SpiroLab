#Projet : SpiroLab
#Auteurs : Lamiss Elhbishy, Thomas Diot, Pierre Gallois, Jules Charlier, Jim Garnier

import flet as ft

from .home_page import home_page
from .recorder_page import recorder_page
from .showroom_page import showroom_page
from .custom_spiro_page import custom_spiro_page

def main(page: ft.Page):
    page.title = "SpiroLab"

    page.fonts = {
        "monospace": "Monospace.ttf"
    }

    def switch_to_recorder(_):
        page.views.clear()
        page.views.append(recorder_page(page, switch_to_showroom_page, switch_to_custom_spiro_page))
        page.update()

    def switch_to_home_page(_):
        page.views.clear()
        page.views.append(home_page(page, go_to_view_record=switch_to_recorder))
        page.update()

    def switch_to_showroom_page(_, audio_path):
        page.views.clear()
        page.views.append(showroom_page(page, audio_path, switch_to_custom_spiro_page))
        page.update()

    def switch_to_custom_spiro_page(_):
        page.views.clear()
        page.views.append(custom_spiro_page(page, switch_to_recorder))
        page.update()

    switch_to_home_page(None)
    
