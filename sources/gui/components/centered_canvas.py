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
    canvas.spiros.pop(spiro_id, None)
    canvas.rotations.pop(spiro_id, None)
    canvas.centers.pop(spiro_id, None)


def _draw(canvas):
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


def _draw_once(canvas):
    draw_id = uuid()
    canvas.last_draw_id = draw_id
    if canvas.r_width is None or canvas.r_height is None:
        print("skipped frame")
        return
    message = BASE_START
    is_first_line_of_spiro = True
    for spiro_id, spiro in canvas.spiros.items():
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
        canvas.clear()
        canvas.ref_page._Page__conn._FletSocketServer__loop.call_soon_threadsafe(canvas.ref_page._Page__conn._FletSocketServer__send_queue.put_nowait, message)
    else:
        return
   


def _clear(canvas):
    canvas.ref_page._Page__conn.send_command(canvas.ref_page._session_id, Command(0, 'clean', [canvas.uid], {}))


def _new_spiro(canvas, center):
    spiro_id = uuid()
    canvas.spiros[spiro_id] = deque(())
    canvas.centers[spiro_id] = center
    return spiro_id, canvas.spiros[spiro_id]

def _on_resize_generate(canvas):
    def on_resize(event):
        canvas.r_width = event.width
        canvas.r_height = event.height
        canvas.clear()
        canvas.draw()
    return on_resize


def _remove_all(canvas):
    canvas.spiros.clear()
    canvas.rotations.clear()
    canvas.centers.clear()