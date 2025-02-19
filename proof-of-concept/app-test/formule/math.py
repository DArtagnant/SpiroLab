from colorsys import hsv_to_rgb
from typing import Optional

def progressive_color(nb_points):
    hue = 0.0
    pas = 3 / nb_points # 2 = nombre de cycles
    while True:
        yield "#{}{}{}".format(*map(lambda n:hex(int(255*n))[2:].zfill(2), hsv_to_rgb(hue, 1, 1)))
        hue = (hue + pas)%1.0

def distance(a: tuple[float, float], b: tuple[float, float]) -> float:
    return ((a[0] - b[0])**2 + (a[1] - b[1])**2)**0.5
