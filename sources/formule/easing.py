#Projet : SpiroLab
#Auteurs : Lamiss Elhbishy, Thomas Diot, Pierre Gallois, Jules Charlier, Jim Garnier

from math import sin, cos, pi

def ease_in_out_cubic(t: float) -> float:
    """
    Fonction d'accélération et de décélération cubique (ease-in-out).
    
    Cette fonction modifie l'intensité de l'animation pour qu'elle commence lentement, 
    accélère au milieu, puis ralentisse à la fin. C'est une interpolation cubique.
    
    Args:
        t (float): Un paramètre de temps entre 0 et 1. Il détermine la progression de l'animation.
        
    Returns:
        float: La valeur interpolée à partir de t.
    """
    if t < 0.5:
        return 4 * t**3  # Phase d'accélération
    else:
        return 1 - ((-2 * t + 2) ** 3) / 2  # Phase de décélération

def ease_in_cubic(t: float) -> float:
    """
    Fonction d'accélération cubique (ease-in).
    
    Cette fonction commence lentement et accélère progressivement de manière cubique.
    
    Args:
        t (float): Un paramètre de temps entre 0 et 1. Il détermine la progression de l'animation.
        
    Returns:
        float: La valeur interpolée à partir de t.
    """
    return t**3  # Accélération cubique

def ease_in_sine(t: float) -> float:
    """
    Fonction d'accélération sinusoidale (ease-in).
    
    Cette fonction commence lentement au début, puis s'accélère en utilisant une courbe sinusoidale.
    
    Args:
        t (float): Un paramètre de temps entre 0 et 1. Il détermine la progression de l'animation.
        
    Returns:
        float: La valeur interpolée à partir de t.
    """
    return 1 - cos((t * pi) / 2)  # Accélération sinusoidale

def ease_out_sine(t: float) -> float:
    """
    Fonction de décélération sinusoidale (ease-out).
    
    Cette fonction commence rapidement et ralentit en utilisant une courbe sinusoidale.
    
    Args:
        t (float): Un paramètre de temps entre 0 et 1. Il détermine la progression de l'animation.
        
    Returns:
        float: La valeur interpolée à partir de t.
    """
    return sin((t * pi) / 2)  # Décélération sinusoidale
