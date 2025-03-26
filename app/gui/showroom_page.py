import flet as ft
from .centered_canvas import centered_canvas
from audio.getter import read_wav
from formule.normalization import normalize_around
from random import randint
from formule import colors_creator
from .spirograph import render_spirograph
from time import sleep

MAX_SPIROS_ON_SCREEN = 4


def compute_spirographs_from_wav(canvas, path):
    print("HAVE PATH", path)
    # TODO : empêcher cette fonction de continuer à s'éxécuter quand on commence à faire autre chose, type afficher un autre spiro
    arrays = read_wav(path)

    large_radii = normalize_around(arrays[0], 70, 60)
    small_radii = normalize_around(arrays[1], 60, 50)
    large_frequencies = normalize_around(arrays[2], 45, 40).astype(int) # On s'assure de n'avoir que des entiers dans la liste
    small_frequencies = normalize_around(arrays[3], 35, 30).astype(int)
    resolution = normalize_around(arrays[4], 35, 15) # TODO : vérifier que ces valeurs ne sont pas débiles

    current_nb_spiros = 0
    for i in range(len(large_radii)):
        # Si le spirographe affiché n'est pas suffisemment différent du dernier, on passe
        # Permet de ne jamais avoir deux spirographes presque identiques d'affilée
        if (i != 0 and
            abs(large_frequencies[i] - large_frequencies[i-1]) <= 4 and
            abs(small_frequencies[i] - small_frequencies[i-1]) <= 4
        ):
            continue

        if current_nb_spiros%MAX_SPIROS_ON_SCREEN == 0:
            canvas.remove_all()

        render_spirograph(
            canvas,
            (randint(-500, 500), randint(-200, 200)), # Position aléatoire

            large_radii[i],
            small_radii[i],
            int(large_frequencies[i]),
            int(small_frequencies[i]),
            resolution[i],

            iter_color = lambda n: colors_creator.smooth_color_generator(["#038AE6", "#86AD2F"], n)
        )

        sleep(0.5)
        canvas.draw_once()
        current_nb_spiros = (current_nb_spiros + 1)%MAX_SPIROS_ON_SCREEN
       

def showroom_page(page: ft.Page, audio_path) -> ft.View:

    cc = centered_canvas(page)

    showroom_page_view = ft.View(
        route= "/dessin",
        controls= [
            ft.Container(
                cc,
                expand= True,
            )
        ]
    )

    page.run_thread(lambda: compute_spirographs_from_wav(cc, audio_path))
    return showroom_page_view

