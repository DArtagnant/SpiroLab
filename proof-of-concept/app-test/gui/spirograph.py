import flet as ft
from flet import canvas as cv
from .math import point_position_from_angles

def spirograph(
    circle: (float, float),
    large_radius: float, 
    small_radius: float, 
    large_angular_velocity: float,
    small_angular_velocity: float,
):
    """Générateur de positions des points du spirographe"""
    circle_angle = 0 # Angle du centre du petit cercle dans le grand cercle
    point_angle = 0 # Angle du point au petit cercle
