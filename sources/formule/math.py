#Projet : SpiroLab
#Auteurs : Lamiss Elhbishy, Thomas Diot, Pierre Gallois, Jules Charlier, Jim Garnier

from math import sin, cos, atan2, pi

def distance(a: tuple[float, float], b: tuple[float, float]) -> float:
    """
    Calcule la distance euclidienne entre deux points dans un plan.

    Cette fonction utilise le théorème de Pythagore pour calculer la distance entre 
    les points 'a' et 'b', représentés sous forme de tuples (x, y).

    Args:
        a (tuple): Le premier point, représenté par un tuple (x, y).
        b (tuple): Le deuxième point, représenté par un tuple (x, y).
        
    Returns:
        float: La distance entre les deux points.
    """
    # Calcul de la distance entre les points a et b en utilisant la formule de Pythagore
    return ((a[0] - b[0])**2 + (a[1] - b[1])**2)**0.5

def calc_point(
        center: tuple[float, float],
        large_radius: float,
        small_radius: float,
        circle_angle: float,
        point_angle: float
    ) -> tuple[tuple[float, float], float, float]:
    """
    Calcule la position d'un point sur un petit cercle en mouvement autour d'un grand cercle.

    Cette fonction calcule la position d'un point qui se trouve sur un petit cercle 
    dont le centre suit une trajectoire circulaire autour du centre d'un grand cercle.

    Args:
        center (tuple[float, float]): Le centre du grand cercle, représenté par un tuple (x, y).
        large_radius (float): Le rayon du grand cercle.
        small_radius (float): Le rayon du petit cercle.
        circle_angle (float): L'angle de rotation du centre du petit cercle autour du grand cercle.
        point_angle (float): L'angle de rotation du point sur le petit cercle par rapport à son centre.

    Returns:
        tuple: La position du point calculée, ainsi que les angles utilisés pour le calcul.
    """
    # Calcule les coordonnées du centre du petit cercle, qui suit un grand cercle
    small_center = (
        center[0] + large_radius * cos(circle_angle),
        center[1] + large_radius * sin(circle_angle),
    )
    
    # Calcule les coordonnées du point sur le petit cercle
    point = (
        small_center[0] + small_radius * cos(point_angle),
        small_center[1] + small_radius * sin(point_angle),
    )
    
    # Retourne la position du point, ainsi que les angles utilisés
    return point, circle_angle, point_angle

def average_angle(a: float, b: float) -> float:
    """
    Calcule l'angle moyen entre deux angles, en prenant en compte l'intervalle le plus court.

    Cette fonction calcule l'angle moyen entre deux angles donnés, en s'assurant 
    que la différence d'angle suivra l'intervalle le plus court entre les deux angles.

    Args:
        a (float): Le premier angle en radians.
        b (float): Le deuxième angle en radians.

    Returns:
        float: L'angle moyen entre a et b, en radians.
    """
    # Vérifie si les deux angles sont opposés (séparés par un demi-cercle), auquel cas retourne l'angle moyen.
    if (a + pi) % (2 * pi) == b:
        return ((a + b) / 2) % (2 * pi)
    else:
        # Utilise la fonction atan2 pour obtenir l'angle moyen, en tenant compte de la somme des sinus et cosinus
        return atan2(sin(a) + sin(b), cos(a) + cos(b))
