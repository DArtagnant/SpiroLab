import flet as ft
from flet import canvas as cv
from formule.math import random_color, point_position_from_angles
import numpy as np

NPOINTS = 1000 # Constante de test

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

    point = point_position_from_angles(
        center, large_radius, small_radius, circle_angle, point_angle
    )

    for _ in range(NPOINTS):
        #yield cv.Circle(*point, 2, ft.Paint(random_color()))

        new_circle_angle = circle_angle + large_angular_velocity
        new_point_angle = point_angle + small_angular_velocity

        new_point = point_position_from_angles(
            center, large_radius, small_radius, new_circle_angle, new_point_angle
        )

        yield cv.Line(*point, *new_point, ft.Paint(random_color()))

        point, circle_angle, point_angle = new_point, new_circle_angle, new_point_angle

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
        canvas.append(line)

def render_spirographs_from_data(cp ,data):
    spiro = tuple(map(lambda x: np.real(x)/20, data[0:6]))
    print(spiro)
    render_spirograph(cp, (spiro[0], spiro[1]),*spiro[2:])