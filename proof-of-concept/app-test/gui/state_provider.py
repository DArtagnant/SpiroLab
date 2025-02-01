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
    if isinstance(shape, cv.Circle):
        shape.x += canvas.state_current_width / 2
        shape.y = -shape.y + canvas.state_current_height / 2
    elif isinstance(shape, cv.Line):
        shape.x1 += canvas.state_current_width / 2
        shape.y1 = -shape.y1 + canvas.state_current_height / 2
        shape.x2 += canvas.state_current_width / 2
        shape.y2 = -shape.y2 + canvas.state_current_height / 2
    else:
        # TODO : logging + warn
        print(f"WARNING : unrecognised shape {shape}, position is not fixed for this shape")

    canvas.shapes.append(shape)

def _generate_auto_resize(canvas: cv.Canvas):

    def auto_resize(event):
        for shape in canvas.shapes:
            patch_x = (-canvas.state_current_width + event.width) / 2
            patch_y = (-canvas.state_current_height + event.height) / 2
            if isinstance(shape, cv.Circle):
                shape.x += patch_x
                shape.y += patch_y
            elif isinstance(shape, cv.Line):
                shape.x1 += patch_x
                shape.y1 += patch_y
                shape.x2 += patch_x
                shape.y2 += patch_y

        canvas.state_current_width = event.width
        canvas.state_current_height = event.height
        canvas.update()

    return auto_resize

