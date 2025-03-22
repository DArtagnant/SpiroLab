import flet as ft
from flet import canvas as cv
from types import MethodType
from itertools import chain
from uuid import uuid1 as uuid
from collections import deque

def centered_canvas(page: ft.Page):
    cc = cv.Canvas([])
    # bypass name mangling
    cc.current_width = None # waiting for first resize
    cc.current_height = None
    cc._get_children = MethodType(_get_children, cc)
    cc.clean = MethodType(_clean, cc)
    cc.shapes = MethodType(NotImplementedError, cc)
    cc._Canvas__shapes = NotImplementedError()
    cc.spiros = {}
    cc.new_spiro = MethodType(_new_spiro, cc)
    cc.on_resize = _resize_handler(cc)
    return cc

def _get_children(canvas):
    """Please clean() before call"""
    if canvas.current_width is None or canvas.current_height is None:
        print("frame sautée")
        return []
    for spiro in canvas.spiros.values():
        for shape in spiro:
            if isinstance(shape, cv.Line):
                yield cv.Line(
                    shape.x1 + canvas.current_width / 2,
                    -shape.y1 + canvas.current_height / 2,
                    shape.x2 + canvas.current_width / 2,
                    -shape.y2 + canvas.current_height / 2,
                    shape.paint
                )
    #return chain(*canvas.spiros.values())

def _clean(canvas):
    super(cv.Canvas, canvas).clean()

def _new_spiro(canvas):
    spiro_id = uuid()
    canvas.spiros[spiro_id] = deque(())
    return canvas.spiros[spiro_id]

def _resize_handler(canvas):
    def auto_resize(event):
        canvas.clean()
        canvas.current_width = event.width
        canvas.current_height = event.height
        canvas.update()
    return auto_resize
