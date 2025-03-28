#Projet : SpiroLab
#Auteurs : Lamiss Elhbishy, Thomas Diot, Pierre Gallois, Jules Charlier, Jim Garnier

from math import sin, cos, pi

def ease_in_out_cubic(t):
    if t < 0.5:
        return 4 * t**3
    else:
        return 1 - ((-2 * t + 2) ** 3) / 2

def ease_in_cubic(t):
    return t**3

def ease_in_sine(t):
    return 1 - cos((t * pi) / 2)

def ease_out_sine(t):
    return sin((t * pi) / 2)