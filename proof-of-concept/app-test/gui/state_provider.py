import flet as ft
from flet import canvas as cv
from types import MethodType

def centered_canvas(page: ft.Page):
    cp = cv.Canvas([])
    cp.on_resize = _generate_auto_resize(cp)
    cp.state_current_width = page.width
    cp.state_current_height = page.height
    cp.append = MethodType(_append, cp)
    return cp

def _append(canvas, shape):
    shape.x += canvas.state_current_width / 2
    shape.y = -shape.y + canvas.state_current_height / 2
    
    # Essai d'adaptation pour les lignes; FIXME
    # shape.x1 += canvas.state_current_width / 2
    # shape.x2 += canvas.state_current_width / 2
    # shape.y1 = -shape.y1 + canvas.state_current_height / 2
    # shape.y2 = -shape.y2 + canvas.state_current_height / 2

    canvas.shapes.append(shape)

def _generate_auto_resize(canvas: cv.Canvas):

    def auto_resize(event):
        for shape in canvas.shapes:
            shape.x += (-canvas.state_current_width + event.width) / 2
            shape.y += (-canvas.state_current_height + event.height) / 2

        canvas.state_current_width = event.width
        canvas.state_current_height = event.height
        canvas.update()

    return auto_resize

