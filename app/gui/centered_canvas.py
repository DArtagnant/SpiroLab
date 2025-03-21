import flet as ft
from flet import canvas as cv
from types import MethodType, SimpleNamespace
from itertools import chain
from uuid import uuid1 as uuid

def centered_canvas(page: ft.Page):
    cp = cv.Canvas([])
    cp.on_resize = _generate_auto_resize(cp)
    cp.state_current_width = page.width
    cp.state_current_height = page.height
    cp.add_spiro = MethodType(_add_spiro, cp)
    cp._redraw_spiros = MethodType(_redraw_spiros, cp)
    cp.spiro_list = {}
    cp._applied_shapes = []
    cp._Canvas__shapes = _generate_iterable_type(cp) # bypass name mangling
    return cp

def _add_spiro(canvas):
    spiro_id = uuid()
    canvas.spiro_list[spiro_id] = []
    def _add_shape(shape):
        print('a')
        canvas.spiro_list[spiro_id].append(shape)
    return _add_shape

def _generate_iterable_type(canvas):
    def f_init(it, canvas):
        it.canvas = canvas
    def f_iter(it):
        return iter(it.canvas._applied_shapes)
    T = type("It", (object,), {
        '__init__': f_init,
        '__iter__': f_iter,
    })
    return T(canvas)

# def _append(canvas, liste, shape):
#     if isinstance(shape, cv.Circle):
#         liste.append(shape)
#         shape.x += canvas.state_current_width / 2
#         shape.y = -shape.y + canvas.state_current_height / 2
#     elif isinstance(shape, cv.Line):
#         liste.append(shape)
#         shape.x1 += canvas.state_current_width / 2
#         shape.y1 = -shape.y1 + canvas.state_current_height / 2
#         shape.x2 += canvas.state_current_width / 2
#         shape.y2 = -shape.y2 + canvas.state_current_height / 2
#     else:
#         # TODO : logging + warn
#         print(f"WARNING : unrecognised shape {shape}, position is not fixed for this shape")

#     liste.append(shape)

def _generate_auto_resize(canvas: cv.Canvas):
    def auto_resize(event):
        my_target = (event.width, event.height)
        canvas.target_size = my_target
        canvas._redraw_spiros(my_target)

    return auto_resize

def _redraw_spiros(canvas, size=None):
    new__applied_shapes = []
    for spiro in canvas.spiro_list.values():
        for shape in spiro:
            if canvas.target_size != size:
                # Cela veut dire qu'un resize plus récent a été demandé
                # Ce code n'a plus de raison de s'exécuter
                return None
            applied_shape = shape
            if isinstance(shape, cv.Circle):
                applied_shape.x = shape.x + size[0] / 2
                applied_shape.y = -shape.y + size[1] / 2
            elif isinstance(shape, cv.Line):
                applied_shape.x1 = shape.x1 + size[0] / 2
                applied_shape.y1 = -shape.y1 + size[1] / 2
                applied_shape.x2 = shape.x2 + size[0] / 2
                applied_shape.y2 = -shape.y2 + size[1] / 2
            new__applied_shapes.append(applied_shape)
    canvas._applied_shapes = new__applied_shapes
    print(len(canvas._applied_shapes))
    print([e for e in canvas._Canvas__shapes])
    canvas.update()
