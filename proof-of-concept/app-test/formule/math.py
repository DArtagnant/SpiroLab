from colorsys import hsv_to_rgb
from math import sin, cos, acos, atan2, pi

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
    return point, circle_angle, point_angle

def average_angle(a, b):
    if (a + pi) % 2*pi == b:
        return ((a+b)/2) % 2*pi
    else:
        return atan2(sin(a) + sin(b), cos(a) + cos(b))

def normal_angle_from_points(
    A: tuple[int, int], B: tuple[int, int], C: tuple[int, int]
):
    # Pour éviter une division par 0, on vérifie que les vecteurs ne sont pas nuls
    if A == B or A == C:
        return None
    AB = (B[0] - A[0], B[1] - A[1])
    AC = (C[0] - A[0], C[1] - A[1])

    dot_prod = AB[0] * AC[0] + AB[1] * AC[1]
    # On réutilise la fonction distance pour la norme, voir plus haut

    angle = acos(dot_prod / (distance(AB, (0,0)) * distance(AC, (0,0))))
    return angle