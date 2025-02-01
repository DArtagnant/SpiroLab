from math import sin, cos
from random import randint

def random_color():
    return hex(randint(0,16777215)).replace("0x", "#")

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
