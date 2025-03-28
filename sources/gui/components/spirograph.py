#Projet : SpiroLab
#Auteurs : Lamiss Elhbishy, Thomas Diot, Pierre Gallois, Jules Charlier, Jim Garnier

import flet as ft
from flet import canvas as cv
from formule.math import distance, calc_point, average_angle
from formule.colors_creator import progressive_color_arc_en_ciel
from collections import deque
from math import pi, lcm
from collections import namedtuple
from typing import Optional, Generator
from .centered_canvas import SpiroLine

# Définition d'une structure nommée (namedtuple) pour représenter un point du spirographe
SpiroPoint = namedtuple("SpiroPoint", ("point", "circle_angle", "point_angle"))

def spirograph(
    center: tuple[float, float],  # Centre du spirographe
    large_radius: float,          # Rayon du grand cercle
    small_radius: float,          # Rayon du petit cercle
    large_angular_velocity: float,  # Vitesse angulaire du grand cercle (en radians par itération)
    small_angular_velocity: float,  # Vitesse angulaire du petit cercle (en radians par itération)
    interpolate_distance_max: float,  # Distance maximale entre deux points pour générer un segment
    nb_points: int,               # Nombre total de points à générer pour le spirographe
    stroke_width: Optional[int] = None,  # Largeur du trait (si non spécifiée, calculée automatiquement)
    iter_color: Optional[Generator[str, None, None]] = None,  # Générateur de couleurs (optionnel)
) -> Generator[SpiroLine, None, None]:
    """
    Génère les positions des points d'un spirographe et les relie par des segments.

    Cette fonction calcule les points d'un spirographe basé sur deux cercles rotatifs : un grand cercle et un petit cercle. 
    Les points sont générés en fonction des vitesses angulaires des cercles et de la distance d'interpolation maximale.

    Args:
        center (tuple[float, float]): Coordonnées du centre du spirographe (x, y).
        large_radius (float): Rayon du grand cercle.
        small_radius (float): Rayon du petit cercle.
        large_angular_velocity (float): Vitesse angulaire du grand cercle (en radians par itération).
        small_angular_velocity (float): Vitesse angulaire du petit cercle (en radians par itération).
        interpolate_distance_max (float): Distance maximale entre deux points pour déclencher une interpolation.
        nb_points (int): Nombre total de points à générer pour le spirographe.
        stroke_width (Optional[int], optional): Largeur du trait (déterminée automatiquement si non fournie).
        iter_color (Optional[Generator[str, None, None]], optional): Générateur de couleurs à appliquer aux segments.

    Yields:
        SpiroLine: Un objet SpiroLine représentant un segment du spirographe avec ses coordonnées, couleur et largeur de trait.
    
    Raises:
        Exception: Si la boucle d'interpolation atteint un nombre excessif d'opérations sans convergence (plus de 10^4).
    
    Notes:
        - La fonction utilise un algorithme d'interpolation pour affiner la courbure du spirographe lorsque les points sont éloignés.
        - Si aucune couleur n'est fournie, un générateur de couleurs en arc-en-ciel est utilisé par défaut.
    """
    print(f"Affichage d'un spiro à {nb_points} points")

    # Détermination de la largeur du trait en fonction du nombre de points (complexité du dessin)
    if stroke_width is None:
        if nb_points >= 1000:
            stroke_width = 2
        elif nb_points >= 500:
            stroke_width = 3
        else:
            stroke_width = 5

    point1 = None  # Point précédent (initialement None)
    point2 = SpiroPoint(None, 0, 0)  # Point actuel (initialement vide)

    # Si aucun générateur de couleurs n'est fourni, on utilise un arc-en-ciel progressif
    if iter_color is None:
        colors = progressive_color_arc_en_ciel(nb_points)
    else:
        colors = iter_color(nb_points)

    for _ in range(nb_points):
        point1 = point2  # Le point précédent devient le point actuel

        # Calcul du prochain point du spirographe avec la fonction 'calc_point'
        point2 = SpiroPoint(*calc_point(
            center,
            large_radius,
            small_radius,
            (point2.circle_angle + large_angular_velocity) % (2 * pi),
            (point2.point_angle + small_angular_velocity) % (2 * pi),
        ))

        # On ignore la suite pour le premier point
        if point1.point is None:
            continue

        to_be_constructed = deque((point1, point2))  # File d'attente pour construire les segments

        operations = 0  # Compteur de tentatives pour éviter les boucles infinies
        while len(to_be_constructed) > 1 and operations < 10**4:
            tbc_point1 = to_be_constructed.popleft()  # Premier point à traiter
            tbc_point2 = to_be_constructed[0]  # Deuxième point dans la file d'attente

            # Si la distance entre les deux points est inférieure à la distance d'interpolation, on génère un segment
            if distance(tbc_point1.point, tbc_point2.point) < interpolate_distance_max:
                yield SpiroLine(
                    point1.point,
                    point2.point,
                    next(colors),  # Couleur suivante
                    stroke_width  # Largeur du trait
                )
            else:
                # Calcul d'un point intermédiaire entre les deux pour affiner la courbe
                middle_point = SpiroPoint(*calc_point(
                    center,
                    large_radius,
                    small_radius,
                    average_angle(tbc_point1.circle_angle, tbc_point2.circle_angle),
                    average_angle(tbc_point1.point_angle, tbc_point2.point_angle),
                ))
                to_be_constructed.appendleft(middle_point)  # Ajout du point intermédiaire à la file d'attente
                to_be_constructed.appendleft(tbc_point1)  # Réintégration du premier point

            operations += 1  # Incrémentation du compteur d'opérations

        # Si le nombre d'opérations dépasse 10 000, une exception est levée pour éviter une boucle infinie
        if operations >= 10**4:
            raise Exception("Unfinished loop")

def render_spirograph(
    canvas: cv.Canvas,  # Le canevas où dessiner le spirographe
    center: tuple[float, float],  # Centre du spirographe
    large_radius: float,  # Rayon du grand cercle
    small_radius: float,  # Rayon du petit cercle
    large_frequency: int,  # Fréquence du grand cercle
    small_frequency: int,  # Fréquence du petit cercle
    interpolate_distance_max: float,  # Distance maximale d'interpolation
    stroke_width: Optional[int] = None,  # Largeur du trait (optionnel)
    iter_color: Optional[Generator[str, None, None]] = None,  # Générateur de couleurs (optionnel)
) -> int:
    """
    Dessine un spirographe sur un canevas en générant et en ajoutant les segments à la file d'attente du canevas.

    Cette fonction utilise la fonction `spirograph` pour calculer les points du spirographe et génère des segments 
    entre chaque paire de points, les ajoutant à une file d'attente sur le canevas pour être affichés.

    Args:
        canvas (cv.Canvas): Le canevas sur lequel le spirographe sera dessiné.
        center (tuple[float, float]): Coordonnées du centre du spirographe (x, y).
        large_radius (float): Rayon du grand cercle.
        small_radius (float): Rayon du petit cercle.
        large_frequency (int): Fréquence du grand cercle (nombre de rotations par unité de temps).
        small_frequency (int): Fréquence du petit cercle (nombre de rotations par unité de temps).
        interpolate_distance_max (float): Distance maximale entre deux points pour générer un segment.
        stroke_width (Optional[int], optional): Largeur du trait (si non fournie, calculée automatiquement).
        iter_color (Optional[Generator[str, None, None]], optional): Générateur de couleurs à appliquer aux segments.

    Returns:
        int: L'identifiant du spirographe créé sur le canevas.

    Notes:
        - La fonction convertit les fréquences des cercles en vitesses angulaires (en radians par itération).
        - Si aucun générateur de couleurs n'est fourni, un générateur de couleurs en arc-en-ciel est utilisé par défaut.
        - Le nombre de points du spirographe est déterminé par le plus petit commun multiple (LCM) des fréquences.
    """

    # Création d'un identifiant pour le spirographe et d'une deque pour les lignes
    spiro_id, spiro_deque = canvas.new_spiro(center)

    # Appel de la fonction spirograph pour générer les points et les lignes
    for line in spirograph(
        center,
        large_radius,
        small_radius,
        2 * pi / large_frequency,  # Conversion de la fréquence en vitesse angulaire
        2 * pi / small_frequency,  # Conversion de la fréquence en vitesse angulaire
        interpolate_distance_max,
        lcm(large_frequency, small_frequency) + 1,  # Limite le nombre de points en fonction du plus petit commun multiple
        stroke_width,
        iter_color,
    ):
        spiro_deque.append(line)  # Ajout de chaque ligne générée au canevas

    return spiro_id  # Retourne l'identifiant du spirographe créé
