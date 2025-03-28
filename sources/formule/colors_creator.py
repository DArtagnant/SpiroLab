#Projet : SpiroLab
#Auteurs : Lamiss Elhbishy, Thomas Diot, Pierre Gallois, Jules Charlier, Jim Garnier

from colorsys import hsv_to_rgb
from random import randint

def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """
    Convertit une couleur en format hexadécimal (ex : "#ACDDDE") en un tuple (R, G, B).
    
    Args:
        hex_color (str): La couleur en format hexadécimal, commençant par un "#" (ex : "#ACDDDE").
        
    Returns:
        tuple[int, int, int]: Un tuple de trois entiers représentant les valeurs RGB de la couleur.
    
    Exemple:
        hex_to_rgb("#ACDDDE") -> (172, 221, 222)
    """
    hex_color = hex_color.lstrip("#")  # Retire le caractère "#" du début de la chaîne.
    # Convertit les sous-chaînes hexadécimales en valeurs entières et retourne un tuple (R, G, B)
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    """
    Convertit un tuple (R, G, B) en une chaîne représentant une couleur en format hexadécimal.
    
    Args:
        rgb (tuple[int, int, int]): Un tuple de trois entiers représentant une couleur (R, G, B).
        
    Returns:
        str: La couleur en format hexadécimal (ex : "#ACDDDE").
    
    Exemple:
        rgb_to_hex((172, 221, 222)) -> "#ACDDDE"
    """
    # Formate les valeurs RGB en une chaîne hexadécimale, avec des valeurs sur deux chiffres pour chaque composant.
    return "#{:02X}{:02X}{:02X}".format(*rgb)

def interpolate_colors(
        color1: tuple[int, int, int],
        color2: tuple[int, int, int],
        t: float
    ) -> tuple[int, int, int]:
    """
    Interpole de manière linéaire entre deux couleurs RGB.
    
    Args:
        color1 (tuple[int, int, int]): La première couleur sous forme de tuple (R, G, B).
        color2 (tuple[int, int, int]): La deuxième couleur sous forme de tuple (R, G, B).
        t (float): Un paramètre de l'interpolation, où t=0 donne color1 et t=1 donne color2.
        
    Returns:
        tuple[int, int, int]: La couleur interpolée entre color1 et color2, sous forme de tuple (R, G, B).
    
    Exemple:
        interpolate_colors((255, 0, 0), (0, 0, 255), 0.5) -> (128, 0, 128)
    """
    # Calcule l'interpolation entre chaque composant RGB
    return (
        int(color1[0] + (color2[0] - color1[0]) * t),
        int(color1[1] + (color2[1] - color1[1]) * t),
        int(color1[2] + (color2[2] - color1[2]) * t),
    )

def smooth_color_generator(colors: str, steps: int, easing=None):
    """
    Génère un flux de couleurs hexadécimales en interpolant doucement entre les couleurs spécifiées.
    
    Cette fonction crée un générateur qui fournit des couleurs intermédiaires entre chaque paire de couleurs, 
    et connecte la dernière couleur à la première pour créer un cycle continu.
    
    Args:
        colors (iterable): Liste de couleurs en format hexadécimal à interpoler.
        steps (int): Le nombre de couleurs intermédiaires à générer entre chaque paire.
        easing (function, optionnel): Une fonction d'easing qui modifie l'interpolation (par défaut linéaire).
        
    Yields:
        str: Une couleur en format hexadécimal à chaque itération.
    
    Exemple:
        smooth_color_generator(["#FF0000", "#00FF00"], 5) -> Génère 5 couleurs entre rouge et vert.
    """
    if easing is None:
        easing = lambda t: t  # Si aucune fonction d'easing n'est fournie, on utilise une interpolation linéaire.

    # Convertir les couleurs hexadécimales en valeurs RGB
    rgb_colors = [hex_to_rgb(c) for c in colors]
    n = len(rgb_colors)  # Nombre de couleurs

    i = 0  # Indice de la couleur de départ
    while True:
        start = rgb_colors[i]
        end = rgb_colors[(i+1) % n]  # Couleur suivante, avec boucle de retour à la première couleur
        for step in range(steps):
            t = step / steps  # Paramètre d'interpolation entre 0 et 1
            rgb_interp = interpolate_colors(start, end, easing(t))  # Interpolation entre start et end
            yield rgb_to_hex(rgb_interp)  # Conversion de la couleur interpolée en hex et émission
        i = (i+1) % n  # Passe à la couleur suivante, en revenant à la première si nécessaire

def progressive_color_arc_en_ciel(nb_points: int):
    """
    Génère un arc-en-ciel progressif de couleurs à partir de la teinte (hue).
    
    Cette fonction crée un flux de couleurs dans le spectre de teintes, allant de 0 à 1.
    
    Args:
        nb_points (int): Le nombre de points (couleurs) à générer dans l'arc-en-ciel.
        
    Yields:
        str: Une couleur en format hexadécimal représentant une couleur de l'arc-en-ciel.
    
    Exemple:
        progressive_color_arc_en_ciel(10) -> Génère 10 couleurs progressives dans un arc-en-ciel.
    """
    hue = 0.0  # Teinte initiale
    pas = 3 / nb_points  # Ajuste la vitesse de l'arc-en-ciel en fonction du nombre de points
    while True:
        # Conversion de la teinte (hue) en RGB puis en hexadécimal, et émission de la couleur
        yield "#{}{}{}".format(*map(lambda n: hex(int(255 * n))[2:].zfill(2), hsv_to_rgb(hue, 1, 1)))
        hue = (hue + pas) % 1.0  # Mise à jour de la teinte, avec boucle sur 1.0

def gen_random_color_scheme(i=None):
    """
    Génère un schéma de couleurs aléatoire en sélectionnant une paire de couleurs prédéfinies.
    
    Si l'indice 'i' est spécifié, il sélectionne une paire spécifique parmi une liste d'intervalles.
    Sinon, une paire est choisie aléatoirement.
    
    Args:
        i (int, optionnel): L'indice de l'intervalle de couleurs à utiliser dans la liste prédéfinie.
        
    Returns:
        function: Une fonction qui génère un schéma de couleurs progressif.
    
    Exemple:
        gen_random_color_scheme() -> Génère un schéma de couleurs aléatoire.
        gen_random_color_scheme(2) -> Utilise l'intervalle d'indice 2 pour générer un schéma.
    """
    intervals = [
        None,
        ("#957DAD", "#FFDFD3"),
        ("#8B52CB", "#F7D903"),
        ("#AA0815", "#3D9BE1"),
        ("#360258", "#AF1D61"),
        ("#FFCE08", "#1259B8"),
        ("#E37324", "#1F1FD1"),
        ("#41BBF4", "#EC4087"),
        ("#88d8b0", "#f96e5a"),
        ("#f56600", "#e026a3"),
        ("#00ff41", "#003b00"),
        ("#772A53", "#E87C5D"),
    ]

    if i is None:
        interval = intervals[randint(0, len(intervals) - 1)]  # Sélection aléatoire
    else:
        interval = intervals[i % (len(intervals) - 1)]  # Sélection basée sur l'indice fourni

    if interval is None:
        return progressive_color_arc_en_ciel  # Retourne la fonction de génération d'arc-en-ciel
    else:
        # Retourne une fonction générant des couleurs interpolées entre les deux couleurs spécifiées.
        return lambda nb_points: smooth_color_generator(interval, nb_points)
