import flet as ft
from flet import canvas as cv
from formule.math import progressive_color, distance, calc_point, average_angle
import numpy as np
from collections import deque
from math import pi, lcm

def spirograph(
    center: tuple[float, float],
    large_radius: float, 
    small_radius: float, 
    large_angular_velocity: float,
    small_angular_velocity: float,
    interpolate_distance_max: float,
    nb_points: int,
):
    print(f"Affichage d'un spiro à {nb_points} points")
    """Générateur de positions des points du spirographe"""
    circle_angle2 = 0 # Angle du centre du petit cercle dans le grand cercle
    point_angle2 = 0 # Angle du point au petit cercle
    circle_angle3 = 0
    point_angle3 = 0

    point1 = None
    point2 = None
    point3 = None
    colors = progressive_color(nb_points)
    for _ in range(nb_points+1):
        point1 = point2
        point2 = point3
        circle_angle1 = circle_angle2
        point_angle1 = point_angle2
        circle_angle2 = circle_angle3
        point_angle2 = point_angle3

        circle_angle3 += large_angular_velocity
        circle_angle3 %= 2*pi
        point_angle3 += small_angular_velocity
        point_angle3 %= 2*pi
        point3 = calc_point(center, large_radius, small_radius, circle_angle3, point_angle3)
        
        # on ignore la suite pour le premier et deuxième point
        if point1 is None: continue

        to_be_constructed = deque(((point1, circle_angle1, point_angle1), (point2, circle_angle2, point_angle2), (point3, circle_angle3, point_angle3)))

        operations = 0
        while len(to_be_constructed) >= 3 and operations < 10**4:
            point1, circle_angle1, point_angle1 = to_be_constructed.popleft()
            point2, circle_angle2, point_angle2 = to_be_constructed[0]
            point3, circle_angle3, point_angle3 = to_be_constructed[1]
            angle_between_points = None
            if angle_between_points is None or angle_between_points < interpolate_distance_max:
                yield cv.Line(*point1, *point2, ft.Paint(next(colors)))
            else:
                # On doit interpoler un point entre point1 et point2
                circle_angle12 = average_angle(circle_angle1, circle_angle2)
                point_angle12 = average_angle(point_angle1, point_angle2)
                point12 = calc_point(center, large_radius, small_radius, circle_angle12, point_angle12)
                to_be_constructed.appendleft((point12, circle_angle12, point_angle12))
                to_be_constructed.appendleft((point1, circle_angle1, point_angle1))
            operations += 1
        if operations >= 10**4:
            # Afin d'éviter une boucle infini qui mange toute la mémoire RAM
            raise Exception("Unfinished loop")

def render_spirograph(
    canvas: cv.Canvas,
    center: tuple[float, float],
    large_radius: float, 
    small_radius: float, 
    large_frequency: int,
    small_frequency: int,
    interpolate_distance_max: float,
):
    for line in spirograph(
        center,
        large_radius,
        small_radius,
        2*pi / large_frequency, # Conversion des fréquences en "vitesse angulaire"
        2*pi / small_frequency,
        interpolate_distance_max,
        lcm(large_frequency, small_frequency) + 1, # Permet de limiter le nombre de calls en donnant le nombre de points exact du spirographe
    ):
        canvas.append(line)

def render_spirographs_from_data(cp, data):
    spiro = tuple(map(lambda x: np.real(x)/50, data[7:13]))
    print(spiro)
    render_spirograph(cp, (spiro[0], spiro[1]),*spiro[2:], 50)