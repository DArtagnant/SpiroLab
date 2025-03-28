#Projet : SpiroLab
#Auteurs : Lamiss Elhbishy, Thomas Diot, Pierre Gallois, Jules Charlier, Jim Garnier

from math import sin, cos, atan2, pi

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