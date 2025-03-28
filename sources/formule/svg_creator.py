#Projet : SpiroLab
#Auteurs : Lamiss Elhbishy, Thomas Diot, Pierre Gallois, Jules Charlier, Jim Garnier

from math import sin, cos
from typing import Optional

# Déclaration du début du fichier SVG, avec des paramètres pour la largeur et la hauteur
HEAD = """<?xml version="1.0" standalone="yes"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
  "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="{width}" height="{height}" version="1.1" xmlns="http://www.w3.org/2000/svg">"""

# Déclaration de la fin du fichier SVG
END = """</svg>"""

# Template pour dessiner une ligne dans le SVG
LINE = """<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{line_width}" />"""

def create_svg_for(
        list_of_points: list,
        center_spiro: tuple[int, int],
        output_path: str,
        marges: int = 20,
        angle: Optional[float] = None,
    ):
    """
    Crée un fichier SVG à partir d'une liste de points représentant des lignes.

    Cette fonction génère un fichier SVG contenant des lignes définies par les points 
    dans `list_of_points`, en prenant en compte une marge pour ajuster les dimensions 
    du fichier final. Un éventuel angle de rotation peut être appliqué à toutes les lignes 
    avant l'écriture dans le fichier. Le fichier SVG est sauvegardé à l'emplacement spécifié 
    par `output_path`.

    Args:
        list_of_points (list): Liste d'objets représentant des lignes, chaque ligne 
                                ayant les attributs `p_from`, `p_to`, `stroke_width`, et `color`.
        center_spiro (tuple): Coordonnées du centre (csx, csy) pour le décalage des points.
        output_path (str): Le chemin du fichier de sortie où le SVG sera enregistré.
        marges (int, optional): Marge autour des lignes dans le SVG. Défaut à 20.
        angle (float, optional): Un angle de rotation à appliquer aux lignes. Défaut à None (pas de rotation).

    Exemple:
        create_svg_for(list_of_points, (300, 300), "output.svg", marges=10, angle=pi/4)
    """
    csx, csy = center_spiro  # Récupère les coordonnées du centre pour décaler les points

    # Ouverture du fichier en mode écriture
    with open(output_path, "w") as file:
        # Initialisation des valeurs maximales et minimales pour déterminer les dimensions du SVG
        max_x = float('-inf')
        max_y = float('-inf')
        min_x = float('+inf')
        min_y = float('+inf')

        # Première boucle pour calculer les dimensions du SVG et appliquer les transformations
        for line in list_of_points:
            # Déplacement des points par rapport au centre de l'espèce
            x1 = line.p_from[0] - csx
            x2 = line.p_to[0] - csx
            y1 = line.p_from[1] - csy
            y2 = line.p_to[1] - csy

            # Si un angle de rotation est spécifié, applique la rotation aux points
            if angle is not None:
                x1p = (x1 * cos(angle) - y1 * sin(angle))
                y1p = (x1 * sin(angle) + y1 * cos(angle))
                x2p = (x2 * cos(angle) - y2 * sin(angle))
                y2p = (x2 * sin(angle) + y2 * cos(angle))
                x1, y1, x2, y2 = x1p, y1p, x2p, y2p

            # Mise à jour des coordonnées minimales et maximales
            min_x = min(min_x, x1, x2)
            max_x = max(max_x, x1, x2)
            max_y = max(max_y, y1, y2)
            min_y = min(min_y, y1, y2)

        # Application des marges autour des coordonnées calculées
        min_x -= marges
        max_x += marges
        max_y += marges
        min_y -= marges

        # Écriture de l'entête SVG avec les dimensions calculées
        file.write(HEAD.format(
            width=max_x - min_x,
            height=max_y - min_y,
        ))

        # Deuxième boucle pour écrire les lignes dans le fichier SVG
        for line in list_of_points:
            # Récupère les coordonnées des points de la ligne
            x1 = line.p_from[0] - csx
            x2 = line.p_to[0] - csx
            y1 = line.p_from[1] - csy
            y2 = line.p_to[1] - csy

            # Applique la rotation si un angle est fourni
            if angle is not None:
                x1p = (x1 * cos(angle) - y1 * sin(angle))
                y1p = (x1 * sin(angle) + y1 * cos(angle))
                x2p = (x2 * cos(angle) - y2 * sin(angle))
                y2p = (x2 * sin(angle) + y2 * cos(angle))
                x1, y1, x2, y2 = x1p, y1p, x2p, y2p

            # Écriture de chaque ligne dans le fichier SVG
            file.write(LINE.format(
                x1=x1 - min_x,
                y1=(max_y - min_y) - (y1 - min_y),
                x2=x2 - min_x,
                y2=(max_y - min_y) - (y2 - min_y),
                line_width=line.stroke_width,
                color=line.color,
            ))

        # Écriture de la fin du fichier SVG
        file.write(END)
