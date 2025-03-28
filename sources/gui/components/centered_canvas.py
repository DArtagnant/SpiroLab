#Projet : SpiroLab
#Auteurs : Lamiss Elhbishy, Thomas Diot, Pierre Gallois, Jules Charlier, Jim Garnier

import flet as ft
from flet import canvas as cv
from types import MethodType
from uuid import uuid1 as uuid
from collections import deque, namedtuple
from flet.core.protocol import Command
from math import cos, sin

SpiroLine = namedtuple("SpiroLine", ("p_from", "p_to", "color", "stroke_width"))

def centered_canvas(page: ft.Page):
    """
    Crée un canevas centré pour dessiner des spirographes. Le canevas est attaché à la page spécifiée
    et permet de dessiner et manipuler les spirographes avec diverses opérations.
    
    Args:
        page (ft.Page): La page Flet sur laquelle le canevas sera ajouté.
    
    Returns:
        cv.Canvas: Un objet canvas Flet configuré avec des méthodes pour dessiner et manipuler les spirographes.
    """
    cc = cv.Canvas([])
    cc.spiros = {}
    cc.ref_page = page
    cc.r_width = None
    cc.r_height = None
    cc.last_draw_id = None
    cc.new_spiro = MethodType(_new_spiro, cc)
    cc.draw = MethodType(_draw, cc)
    cc.draw_once = MethodType(_draw_once, cc)
    cc.clear = MethodType(_clear, cc)
    cc.rotations = {}
    cc.centers = {}
    cc.on_resize = _on_resize_generate(cc)
    cc.remove_all = MethodType(_remove_all, cc)
    return cc

BASE_START = """{"action": "pageControlsBatch","payload": ["""
BASE_END = """]}"""

def _remove(canvas, spiro_id):
    """
    Supprime un spirographe du canevas en retirant ses lignes, rotations et centres associés.
    
    Args:
        canvas (cv.Canvas): Le canevas sur lequel le spirographe est dessiné.
        spiro_id (str): L'identifiant unique du spirographe à supprimer.
    """
    canvas.spiros.pop(spiro_id, None)
    canvas.rotations.pop(spiro_id, None)
    canvas.centers.pop(spiro_id, None)


def _draw(canvas):
    """
    Dessine toutes les lignes des spirographes présents dans le canevas. Ce dessin est mis à jour à chaque appel.
    
    Args:
        canvas (cv.Canvas): Le canevas sur lequel les spirographes sont dessinés.
    """
    draw_id = uuid()
    canvas.last_draw_id = draw_id
    if canvas.r_width is None or canvas.r_height is None:
        print("skipped frame")
        return
    for spiro_id, spiro in canvas.spiros.items():
        message = BASE_START
        is_first_line_of_spiro = True
        for line in spiro:
            # On teste si on est toujours le dernier draw a avoir été appelé
            if canvas.last_draw_id != draw_id:
                return

            # Json n'aime pas les , mal placés
            if not is_first_line_of_spiro:
                message += ","
            else:
                is_first_line_of_spiro = False

            # Calculs de la véritable position
            
            x1 = line.p_from[0]
            y1 = line.p_from[1]
            x2 = line.p_to[0]
            y2 = line.p_to[1]

            angle = canvas.rotations.get(spiro_id, None)
            if angle is not None:
                cx, cy = canvas.centers[spiro_id]
                x1_p = ((x1 - cx) * cos(angle) - (y1 - cy) * sin(angle)) + cx
                y1_p = ((x1 - cx) * sin(angle) + (y1 - cy) * cos(angle)) + cy
                x2_p = ((x2 - cx) * cos(angle) - (y2 - cy) * sin(angle)) + cx
                y2_p = ((x2 - cx) * sin(angle) + (y2 - cy) * cos(angle)) + cy
                x1, y1, x2, y2 = x1_p, y1_p, x2_p, y2_p

            x1 += canvas.r_width / 2
            y1 = -y1 + canvas.r_height / 2
            x2 += canvas.r_width / 2
            y2 = -y2 + canvas.r_height / 2
            
            message += """{
                    "action": "addPageControls",
                    "payload": {
                        "controls": [
                            {
                                "t": "line",
                                "i": "_custom_""" + uuid().hex + """\",
                                "p": \"""" + str(canvas._Control__uid) + """\",
                                "c": [],
                                "paint": "{\\"color\\":\\\"""" + line.color + """\\",\\"stroke_cap\\":\\"round\\",\\"stroke_join\\":\\"round\\",\\"stroke_width\\":""" + str(line.stroke_width) + """}",
                                "x1": \"""" + str(x1) + """\",
                                "x2": \"""" + str(x2) + """\",
                                "y1": \"""" + str(y1) + """\",
                                "y2": \"""" + str(y2) + """\"
                            }
                        ],
                        "trimIDs": []
                    }
                    }"""
        message += BASE_END
        # On teste encore une fois si on est le dernier draw pour éviter une trace
        if canvas.last_draw_id == draw_id:
            canvas.ref_page._Page__conn._FletSocketServer__loop.call_soon_threadsafe(canvas.ref_page._Page__conn._FletSocketServer__send_queue.put_nowait, message)
        else:
            return
        
def _remove(canvas, spiro_id):
    """
    Supprime un spirographe spécifique du canevas en retirant son identifiant, 
    ses rotations et ses centres des dictionnaires associés.

    Args:
        canvas (cv.Canvas): Le canevas sur lequel le spirographe est dessiné.
        spiro_id (str): L'identifiant du spirographe à supprimer.
    """
    canvas.spiros.pop(spiro_id, None)
    canvas.rotations.pop(spiro_id, None)
    canvas.centers.pop(spiro_id, None)


def _draw(canvas):
    """
    Dessine tous les spirographes présents sur le canevas en envoyant les informations
    de dessin sous forme de messages JSON à la page associée. Chaque spirographe est constitué
    de lignes, et les calculs de rotation et de position sont appliqués avant d'envoyer les données.
    
    Args:
        canvas (cv.Canvas): Le canevas sur lequel les spirographes sont dessinés.
    """
    draw_id = uuid()
    canvas.last_draw_id = draw_id
    if canvas.r_width is None or canvas.r_height is None:
        print("skipped frame")
        return

    for spiro_id, spiro in canvas.spiros.items():
        message = BASE_START
        is_first_line_of_spiro = True

        for line in spiro:
            # On teste si on est toujours le dernier draw à avoir été appelé
            if canvas.last_draw_id != draw_id:
                return

            # Format JSON correct pour éviter les erreurs de syntaxe
            if not is_first_line_of_spiro:
                message += ","
            else:
                is_first_line_of_spiro = False

            # Calcul des positions réelles après application des rotations
            x1, y1 = line.p_from
            x2, y2 = line.p_to

            # Applique la rotation si nécessaire
            angle = canvas.rotations.get(spiro_id, None)
            if angle is not None:
                cx, cy = canvas.centers[spiro_id]
                x1_p = ((x1 - cx) * cos(angle) - (y1 - cy) * sin(angle)) + cx
                y1_p = ((x1 - cx) * sin(angle) + (y1 - cy) * cos(angle)) + cy
                x2_p = ((x2 - cx) * cos(angle) - (y2 - cy) * sin(angle)) + cx
                y2_p = ((x2 - cx) * sin(angle) + (y2 - cy) * cos(angle)) + cy
                x1, y1, x2, y2 = x1_p, y1_p, x2_p, y2_p

            # Applique un décalage pour que le centre du canevas soit à (0,0)
            x1 += canvas.r_width / 2
            y1 = -y1 + canvas.r_height / 2
            x2 += canvas.r_width / 2
            y2 = -y2 + canvas.r_height / 2

            message += """{
                    "action": "addPageControls",
                    "payload": {
                        "controls": [
                            {
                                "t": "line",
                                "i": "_custom_""" + uuid().hex + """\",
                                "p": \"""" + str(canvas._Control__uid) + """\",
                                "c": [],
                                "paint": "{\\"color\\":\\\"""" + line.color + """\\",\\"stroke_cap\\":\\"round\\",\\"stroke_join\\":\\"round\\",\\"stroke_width\\":""" + str(line.stroke_width) + """}",
                                "x1": \"""" + str(x1) + """\",
                                "x2": \"""" + str(x2) + """\",
                                "y1": \"""" + str(y1) + """\",
                                "y2": \"""" + str(y2) + """\"
                            }
                        ],
                        "trimIDs": []
                    }
                    }"""
        message += BASE_END

        # Vérification finale pour ne pas envoyer un message obsolète
        if canvas.last_draw_id == draw_id:
            # Demande la mise à jour du Canvas à Flutter
            canvas.ref_page._Page__conn._FletSocketServer__loop.call_soon_threadsafe(
                canvas.ref_page._Page__conn._FletSocketServer__send_queue.put_nowait, message)
        else:
            return


def _draw_once(canvas):
    """
    Dessine tous les spirographes présents sur le canevas une seule fois, sans boucle continue,
    en envoyant les informations de dessin sous forme de messages JSON. Cette fonction est
    similaire à `_draw`, mais elle envoit la commande de dessin que lorsque tous les spirographes
    du canvas ont été calculés.

    Args:
        canvas (cv.Canvas): Le canevas sur lequel les spirographes sont dessinés.
    """
    draw_id = uuid()
    canvas.last_draw_id = draw_id
    if canvas.r_width is None or canvas.r_height is None:
        print("skipped frame")
        return

    message = BASE_START
    is_first_line_of_spiro = True

    for spiro_id, spiro in canvas.spiros.items():
        for line in spiro:
            # Vérification pour s'assurer que nous sommes toujours le dernier dessin appelé
            if canvas.last_draw_id != draw_id:
                return

            # Formatage correct du JSON pour éviter les erreurs
            if not is_first_line_of_spiro:
                message += ","
            else:
                is_first_line_of_spiro = False

            # Calcul des positions réelles après application des rotations
            x1, y1 = line.p_from
            x2, y2 = line.p_to

            # Applique la rotation si elle est présente
            angle = canvas.rotations.get(spiro_id, None)
            if angle is not None:
                cx, cy = canvas.centers[spiro_id]
                x1_p = ((x1 - cx) * cos(angle) - (y1 - cy) * sin(angle)) + cx
                y1_p = ((x1 - cx) * sin(angle) + (y1 - cy) * cos(angle)) + cy
                x2_p = ((x2 - cx) * cos(angle) - (y2 - cy) * sin(angle)) + cx
                y2_p = ((x2 - cx) * sin(angle) + (y2 - cy) * cos(angle)) + cy
                x1, y1, x2, y2 = x1_p, y1_p, x2_p, y2_p

            # Ajuste de l'origine du canevas pour que (0,0) soit au centre
            x1 += canvas.r_width / 2
            y1 = -y1 + canvas.r_height / 2
            x2 += canvas.r_width / 2
            y2 = -y2 + canvas.r_height / 2

            message += """{
                    "action": "addPageControls",
                    "payload": {
                        "controls": [
                            {
                                "t": "line",
                                "i": "_custom_""" + uuid().hex + """\",
                                "p": \"""" + str(canvas._Control__uid) + """\",
                                "c": [],
                                "paint": "{\\"color\\":\\\"""" + line.color + """\\",\\"stroke_cap\\":\\"round\\",\\"stroke_join\\":\\"round\\",\\"stroke_width\\":""" + str(line.stroke_width) + """}",
                                "x1": \"""" + str(x1) + """\",
                                "x2": \"""" + str(x2) + """\",
                                "y1": \"""" + str(y1) + """\",
                                "y2": \"""" + str(y2) + """\"
                            }
                        ],
                        "trimIDs": []
                    }
                    }"""
    message += BASE_END
    # Envoi du message si ce dessin est encore valide
    if canvas.last_draw_id == draw_id:
        canvas.clear()  # Efface tout le contenu du canevas avant de redessiner
        canvas.ref_page._Page__conn._FletSocketServer__loop.call_soon_threadsafe(
            canvas.ref_page._Page__conn._FletSocketServer__send_queue.put_nowait, message)
    else:
        return


def _clear(canvas):
    """
    Efface toutes les commandes de dessin sur le canevas en envoyant une commande de nettoyage
    à la page associée. Cette fonction est utilisée pour supprimer tout le contenu visuel du canevas.
    
    Args:
        canvas (cv.Canvas): Le canevas à effacer.
    """
    canvas.ref_page._Page__conn.send_command(canvas.ref_page._session_id, Command(0, 'clean', [canvas.uid], {}))


def _new_spiro(canvas, center):
    """
    Crée un nouveau spirographe sur le canevas avec un identifiant unique et un centre spécifié.
    
    Args:
        canvas (cv.Canvas): Le canevas sur lequel créer un spirographe.
        center (tuple): Le centre du spirographe sous la forme (x, y).
    
    Returns:
        tuple: Un tuple contenant l'identifiant du spirographe et une file de lignes associée à ce spirographe.
    """
    spiro_id = uuid()
    canvas.spiros[spiro_id] = deque(())
    canvas.centers[spiro_id] = center
    return spiro_id, canvas.spiros[spiro_id]


def _on_resize_generate(canvas):
    """
    Crée et retourne une fonction de gestion de redimensionnement pour le canevas.
    Lorsque le canevas est redimensionné, cette fonction ajuste les dimensions internes
    du canevas et redessine le contenu.

    Args:
        canvas (cv.Canvas): Le canevas dont la taille doit être mise à jour lors du redimensionnement.
    
    Returns:
        function: Une fonction qui gère l'événement de redimensionnement du canevas.
    """
    def on_resize(event):
        canvas.r_width = event.width
        canvas.r_height = event.height
        canvas.clear()
        canvas.draw()

    return on_resize


def _remove_all(canvas):
    """
    Supprime tous les spirographes, rotations et centres du canevas du côté python.

    Args:
        canvas (cv.Canvas): Le canevas à nettoyer.
    """
    canvas.spiros.clear()
    canvas.rotations.clear()
    canvas.centers.clear()

