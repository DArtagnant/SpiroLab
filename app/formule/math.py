from colorsys import hsv_to_rgb
from math import sin, cos, atan2, pi

def progressive_color(nb_points):
    hue = 0.0
    pas = 3 / nb_points # 2 = nombre de cycles
    while True:
        yield "#{}{}{}".format(*map(lambda n:hex(int(255*n))[2:].zfill(2), hsv_to_rgb(hue, 1, 1)))
        hue = (hue + pas)%1.0

def distance(a: tuple[float, float], b: tuple[float, float]) -> float:
    return ((a[0] - b[0])**2 + (a[1] - b[1])**2)**0.5


def calc_point(center, large_radius, small_radius, circle_angle, point_angle):
    small_center = (
        center[0] + large_radius*cos(circle_angle),
        center[1] + large_radius*sin(circle_angle),
    )
    
    point = (
        small_center[0] + small_radius*cos(point_angle),
        small_center[1] + small_radius*sin(point_angle),
    )
    return point

def average_angle(a, b):
    if (a + pi) % 2*pi == b:
        return ((a+b)/2) % 2*pi
    else:
        return atan2(sin(a) + sin(b), cos(a) + cos(b))