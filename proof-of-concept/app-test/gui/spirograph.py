import flet as ft
from flet import canvas as cv
from formule.math import progressive_color, distance
import numpy as np
from math import sin, cos
from itertools import pairwise

NBPOINTS = 300 # Constante de test
CONSIDER_SAME = (20, 20)

DISTANCE_MAX = 100

#TODO detecter lorsqu'on a fait un tour complet
def spirograph(
    center: tuple[float, float],
    large_radius: float, 
    small_radius: float, 
    large_angular_velocity: float,
    small_angular_velocity: float,
):
    """Générateur de positions des points du spirographe"""
    circle_angle = 0 # Angle du centre du petit cercle dans le grand cercle
    point_angle = 0 # Angle du point au petit cercle

    previous_point = None
    point = None
    colors = progressive_color(NBPOINTS)

    for _ in range(NBPOINTS):
        previous_point = point
        previous_circle_angle = circle_angle
        previous_point_angle = point_angle
        circle_angle += large_angular_velocity
        point_angle += small_angular_velocity

        point = calc_point(center, large_radius, small_radius, circle_angle, point_angle)
        
        # on ignore la suite pour le premier point
        if previous_point is None: continue

        for point1, point2 in pairwise(interpolate(center, large_radius, small_radius, previous_point, point, previous_circle_angle, previous_point_angle, circle_angle, point_angle)):
            yield cv.Line(*point1, *point2, ft.Paint(next(colors)))

def interpolate(center, large_radius, small_radius, point1, point2, circle_angle1, point_angle1, circle_angle2, point_angle2):
    if distance(point1, point2) < DISTANCE_MAX:
        yield point1
        yield point2
    else:
        circle_angle3 = (circle_angle1 + circle_angle2)/2
        point_angle3 = (point_angle1 + point_angle2)/2
        point3 = calc_point(center, large_radius, small_radius, circle_angle3, point_angle3)
        yield point1
        yield from interpolate(center, large_radius, small_radius, point1, point3, circle_angle1, point_angle1, circle_angle3, point_angle3)
        yield from interpolate(center, large_radius, small_radius, point3, point2, circle_angle3, point_angle3, circle_angle2, point_angle2)
        yield point2

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


def render_spirograph(
    canvas: cv.Canvas,
    center: tuple[float, float],
    large_radius: float, 
    small_radius: float, 
    large_angular_velocity: float,
    small_angular_velocity: float,
):
    for line in spirograph(
        center,
        large_radius,
        small_radius,
        large_angular_velocity,
        small_angular_velocity
    ):
        # TODO : interpolation entre les points avec scipy.interpolate
        canvas.append(line)

def render_spirographs_from_data(cp ,data):
    spiro = tuple(map(lambda x: np.real(x)/50, data[7:13]))
    print(spiro)
    render_spirograph(cp, (spiro[0], spiro[1]),*spiro[2:])