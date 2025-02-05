import flet as ft
from flet import canvas as cv
from types import MethodType

def centered_canvas(get_height_fn= None):
    cp = cv.Canvas([], expand=True)
    cp.on_resize = _generate_auto_resize(cp)
    cp.state_current_width = 0
    cp.state_current_height = 0
    cp.append = MethodType(_append, cp)
    cp.state_get_height = get_height_fn
    return cp

def _append(canvas, shape):
    if isinstance(shape, cv.Circle):
        shape.state_absolute_x = shape.x
        shape.state_absolute_y = shape.y
        shape.x += canvas.state_current_width / 2
        shape.y = -shape.y + canvas.state_current_height / 2
    elif isinstance(shape, cv.Line):
        shape.state_absolute_x1 = shape.x1
        shape.state_absolute_y1 = shape.y1
        shape.state_absolute_x2 = shape.x2
        shape.state_absolute_y2 = shape.y2
        shape.x1 += canvas.state_current_width / 2
        shape.y1 = -shape.y1 + canvas.state_current_height / 2
        shape.x2 += canvas.state_current_width / 2
        shape.y2 = -shape.y2 + canvas.state_current_height / 2
    else:
        # TODO : logging + warn
        print(f"WARNING : unrecognised shape {shape}, position is not fixed for this shape")

    canvas.shapes.append(shape)

def _generate_auto_resize(canvas: cv.Canvas):
    # représente la taille la plus à jour à viser lors du changement de taille de fenêtre
    # C'est une variable non locale, commune à tous les callbacks appelés par un même canvas
    target_size = None

    def auto_resize(event):
        nonlocal target_size
        my_width = event.width
        if canvas.state_get_height is not None:
            my_height = canvas.state_get_height()
        else:
            my_height = event.height
        
        my_target = (my_width, my_height)
        target_size = my_target
        print(my_target)
        for shape in canvas.shapes:
            if target_size != my_target:
                # Cela veut dire qu'un resize plus recent a été demandé
                # Ce code n'a plus de raison de s'executer
                return None
            if isinstance(shape, cv.Circle):
                shape.x = shape.state_absolute_x + my_width / 2
                shape.y = -shape.state_absolute_y + my_height / 2
            elif isinstance(shape, cv.Line):
                shape.x1 = shape.state_absolute_x1 + my_width / 2
                shape.y1 = -shape.state_absolute_y1 + my_height / 2
                shape.x2 = shape.state_absolute_x2 + my_width / 2
                shape.y2 = -shape.state_absolute_y2 + my_height / 2
        canvas.state_current_width = my_width
        canvas.state_current_height = my_height
        canvas.update()

    return auto_resize

