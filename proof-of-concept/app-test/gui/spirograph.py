import flet as ft
from flet import canvas as cv
from formule.math import progressive_color, distance, calc_point, average_angle, normal_angle_from_points
import numpy as np
from collections import deque
from math import pi, lcm
from collections import namedtuple

SpiroPoint = namedtuple("SpiroPoint", ("point", "circle_angle", "point_angle"))

def spirograph(
    center: tuple[float, float],
    large_radius: float, 
    small_radius: float, 
    large_angular_velocity: float,
    small_angular_velocity: float,
    interpolate_angle_max: float,
    nb_points: int,
):
    print(f"Affichage d'un spiro à {nb_points} points")
    """Générateur de positions des points du spirographe"""
    spoint1 = SpiroPoint(None, 0, 0)
    spoint2 = SpiroPoint(None, 0, 0)
    spoint3 = SpiroPoint(None, 0, 0)

    colors = progressive_color(nb_points)
    for _ in range(nb_points + 1):
        spoint1 = spoint2
        spoint2 = spoint3

        spoint3 = SpiroPoint(*calc_point(
            center,
            large_radius,
            small_radius,
            (spoint3.circle_angle + large_angular_velocity) % 2 * pi,
            (spoint3.point_angle + small_angular_velocity) % 2 * pi,
        ))
        
        # on ignore la suite pour le premier et deuxième point
        if spoint1.point is None: continue

        to_be_constructed = deque((spoint1, spoint2, spoint3))

        operations = 0
        while len(to_be_constructed) >= 3 and operations < 10**4:
            # tpoint = to_be_constructed point
            tpoint1 = to_be_constructed.popleft()
            tpoint2 = to_be_constructed[0]
            tpoint3 = to_be_constructed[1]
            angle_between_points = normal_angle_from_points(tpoint1.point, tpoint2.point, tpoint3.point)
            print(tpoint1, "\n", tpoint2, "\n", tpoint3)
            print(angle_between_points, abs(angle_between_points - pi), interpolate_angle_max)
            if angle_between_points is None or abs(angle_between_points - pi) < interpolate_angle_max:
                print("ouh")
                yield cv.Line(*tpoint1.point, *tpoint2.point, ft.Paint(next(colors)))
            else:
                print("aaaah")
                # On doit interpoler un point entre point1 et point2
                middle_tpoint = SpiroPoint(*calc_point(
                    center,
                    large_radius,
                    small_radius,
                    average_angle(tpoint1.circle_angle, tpoint2.circle_angle),
                    average_angle(tpoint1.point_angle, tpoint2.point_angle),
                ))
                to_be_constructed.appendleft(middle_tpoint)
                to_be_constructed.appendleft(tpoint1)
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