import flet as ft
from flet import canvas as cv
from formule.math import progressive_color, distance, calc_point, average_angle
import numpy as np
from collections import deque
from math import pi, lcm
from collections import namedtuple
from typing import Optional

SpiroPoint = namedtuple("SpiroPoint", ("point", "circle_angle", "point_angle"))

#TODO detecter lorsqu'on a fait un tour complet
def spirograph(
    center: tuple[float, float],
    large_radius: float, 
    small_radius: float, 
    large_angular_velocity: float,
    small_angular_velocity: float,
    interpolate_distance_max: float,
    nb_points: int,
    stroke_width: Optional[int] = None,
):
    """Générateur de positions des points du spirographe"""
    print(f"Affichage d'un spiro à {nb_points} points")

    if stroke_width is None:
        # On définit le stroke à partir du nombre de points, qui définit environ la complexité du spirographe
        if nb_points >= 1000:
            stroke_width = 2
        elif nb_points >= 500:
            stroke_width = 3
        else:
            stroke_width = 5

    point1 = None
    point2 = SpiroPoint(None, 0, 0)
    colors = progressive_color(nb_points)
    for _ in range(nb_points):
        point1 = point2

        point2 = SpiroPoint(*calc_point(
            center,
            large_radius,
            small_radius,
            (point2.circle_angle + large_angular_velocity) % (2 * pi),
            (point2.point_angle + small_angular_velocity) % (2 * pi),
        ))

        # on ignore la suite pour le premier point
        if point1.point is None: continue

        to_be_constructed = deque((point1, point2))

        operations = 0
        while len(to_be_constructed) > 1 and operations < 10**4:
            tbc_point1 = to_be_constructed.popleft()
            tbc_point2 = to_be_constructed[0]
            if distance(tbc_point1.point, tbc_point2.point) < interpolate_distance_max:
                yield cv.Line(*point1.point, *point2.point,
                    ft.Paint(
                        next(colors),
                        stroke_width=stroke_width,
                        stroke_cap=ft.StrokeCap.ROUND,
                        stroke_join=ft.StrokeJoin.ROUND,
                    ))
            else:
                middle_point = SpiroPoint(*calc_point(
                    center,
                    large_radius,
                    small_radius,
                    average_angle(tbc_point1.circle_angle, tbc_point2.circle_angle),
                    average_angle(tbc_point1.point_angle, tbc_point2.point_angle),
                ))
                to_be_constructed.appendleft(middle_point)
                to_be_constructed.appendleft(tbc_point1)
            operations += 1
        if operations >= 10**4:
            # Afin d'éviter une boucle infinie qui mange toute la mémoire RAM
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
    spiro_deque = canvas.new_spiro()
    for line in spirograph(
        center,
        large_radius,
        small_radius,
        2*pi / large_frequency, # Conversion des fréquences en "vitesse angulaire"
        2*pi / small_frequency,
        interpolate_distance_max,
        lcm(large_frequency, small_frequency) + 1, # Permet de limiter le nombre de calls en donnant le nombre de points exact du spirographe
    ):
        spiro_deque.append(line)

def render_spirographs_from_data(cp, data):
    spiro = tuple(map(lambda x: np.real(x)/50, data[7:13]))
    print(spiro)
    render_spirograph(cp, (spiro[0], spiro[1]),*spiro[2:], 50)