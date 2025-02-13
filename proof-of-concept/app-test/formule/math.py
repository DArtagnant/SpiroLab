from math import sin, cos
from colorsys import hsv_to_rgb

def random_color():
    hue = 0.0
    while True:
        yield "#{}{}{}".format(*map(lambda n:hex(int(255*n))[2:].zfill(2), hsv_to_rgb(hue, 1, 1)))
        hue = (hue + 0.02)%1.0

# A priori, le centre du grand cercle est en 0,0 (cartésien)
def point_position_from_angles(
    center: tuple[float, float],
    large_radius: float, 
    small_radius: float,
    circle_angle: float,
    point_angle: float,
):
    small_center = (
        center[0] + large_radius*cos(circle_angle),
        center[1] + large_radius*sin(circle_angle),
    )

    point = (
        small_center[0] + small_radius*cos(point_angle),
        small_center[1] + small_radius*sin(point_angle),
    )

    return point
