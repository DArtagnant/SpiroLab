import flet as ft
from flet import canvas as cv
from types import MethodType
from itertools import chain
from uuid import uuid1 as uuid
from collections import deque, namedtuple
from flet.core.protocol import Command

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
    cc.clear = MethodType(_clear, cc)
    cc.on_resize = _on_resize_generate(cc)
    return cc

BASE_START = """{"action": "pageControlsBatch","payload": ["""
BASE_END = """]}"""


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
            x1 = line.p_from[0] + canvas.r_width / 2
            y1 = -line.p_from[1] + canvas.r_height / 2
            x2 = line.p_to[0] + canvas.r_width / 2
            y2 = -line.p_to[1] + canvas.r_height / 2
            
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
            
def _clear(canvas):
    canvas.ref_page._Page__conn.send_command(canvas.ref_page._session_id, Command(0, 'clean', [canvas.uid], {}))


def _new_spiro(canvas):
    spiro_id = uuid()
    canvas.spiros[spiro_id] = deque(())
    return canvas.spiros[spiro_id]

def _on_resize_generate(canvas):
    def on_resize(event):
        canvas.r_width = event.width
        canvas.r_height = event.height
        canvas.clear()
        canvas.draw()
    return on_resize
