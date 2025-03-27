import flet as ft
from .components.centered_canvas import centered_canvas
from audio.getter import read_wav
from formule.normalization import normalize_around
from random import randint
from formule import colors_creator
from .components.spirograph import render_spirograph
from time import sleep
from formule import easing

MAX_SPIROS_ON_SCREEN = 4
MARGE = 50

def compute_spirographs_from_wav(page, canvases, containers, path):
    # TODO : empêcher cette fonction de continuer à s'éxécuter quand on commence à faire autre chose, type afficher un autre spiro
    arrays = read_wav(path)

    large_radii = normalize_around(arrays[0], 70, 60)
    small_radii = normalize_around(arrays[1], 60, 50)
    large_frequencies = normalize_around(arrays[2], 45, 40).astype(int) # On s'assure de n'avoir que des entiers dans la liste
    small_frequencies = normalize_around(arrays[3], 35, 30).astype(int)
    resolution = normalize_around(arrays[4], 60, 15) # TODO : vérifier que ces valeurs ne sont pas débiles

    current_nb_spiros = 0
    j = 0
    for i in range(len(large_radii)):
        if page.current_view_name != "showroom":
            return
        
        # Si le spirographe affiché n'est pas suffisemment différent du dernier, on passe
        # Permet de ne jamais avoir deux spirographes presque identiques d'affilée
        if (i != 0 and
            abs(large_frequencies[i] - large_frequencies[i-1]) <= 4 and
            abs(small_frequencies[i] - small_frequencies[i-1]) <= 4
        ):
            continue

        while page.width is None or page.height is None:
            print("double skipped frame")
            page.update()
            sleep(0.01)

        before = j%len(canvases)    
        now = (j+1)%len(canvases)
        
        render_spirograph(
            canvases[before],
            (randint(MARGE, int(page.width) - MARGE), randint(int(-page.height) + MARGE, -MARGE)), # Position aléatoire

            large_radii[i],
            small_radii[i],
            int(large_frequencies[i]),
            int(small_frequencies[i]),
            resolution[i],

            iter_color = colors_creator.gen_random_color_scheme()
        )

        canvases[before].draw_once()
        
        n_steps = 250
        for step in range(n_steps):
            t = step / n_steps
            containers[before].opacity = easing.ease_in_sine(t)
            containers[now].opacity = 1 - easing.ease_out_sine(t)
            page.update()
            sleep(0.01)

        containers[before].opacity = 1
        canvases[now].remove_all()
        page.update()
        current_nb_spiros = (current_nb_spiros + 1)%MAX_SPIROS_ON_SCREEN
        j += 1

def showroom_page(page: ft.Page, audio_path, custom_spiro) -> ft.View:
    page.current_view_name = "showroom"
    cc1 = centered_canvas(page)
    cc2 = centered_canvas(page)
    cc3 = centered_canvas(page)

    showroom_page_view = ft.View(
        route= "/dessin",
        controls= [
            ft.Stack([
                ccc1 := ft.Container(cc1, expand=True),
                ccc2 := ft.Container(cc2, expand=True),
                ccc3 := ft.Container(cc3, expand=True),
            ],
            expand=True)
        ],
    )

    showroom_page_view.floating_action_button = ft.FloatingActionButton(text="Construire son propre spirographe", icon=ft.Icons.BRUSH, on_click=custom_spiro)
    page.run_thread(lambda: compute_spirographs_from_wav(page, [cc1, cc2, cc3], [ccc1, ccc2, ccc3], audio_path))
    return showroom_page_view

