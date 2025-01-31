from math import sin, cos

# A priori, le centre du grand cercle est en 0,0 (cartésien)
def point_position_from_angles(
    center: (float, float),
    large_radius: float, 
    small_radius: float,
    circle_angle: float,
    point_angle: float,
):
    small_center = center + large_radius*(cos(circle_angle), sin(circle_angle))
