#Projet : SpiroLab
#Auteurs : Lamiss Elhbishy, Thomas Diot, Pierre Gallois, Jules Charlier, Jim Garnier

import numpy as np
from math import exp

def normalize_around(array: np.ndarray, value: float, excentricity: float) -> np.ndarray:
    """
    Normalise un tableau autour d'une valeur spécifiée en utilisant une fonction logistique.

    Cette fonction normalise les valeurs d'un tableau de manière à ce que leurs 
    nouvelles valeurs soient centrées autour de la valeur donnée, tout en appliquant 
    une fonction logistique pour restreindre les valeurs à un intervalle défini par 
    l'excentricité (qui détermine l'étendue de la normalisation).

    Args:
        array (np.ndarray): Un tableau de valeurs à normaliser.
        value (float): La valeur autour de laquelle normaliser les données.
        excentricity (float): L'excentricité qui définit l'intervalle de normalisation, 
                               c'est-à-dire la plage dans laquelle les valeurs normalisées 
                               seront restreintes.

    Returns:
        np.ndarray: Le tableau normalisé, centré autour de la valeur spécifiée, 
                    avec les valeurs restreintes par l'excentricité.
    """
    # Supposons que les données sont centrées autour de zéro, donc on prend la valeur maximale
    # de l'absolu pour normaliser par rapport à l'intervalle.
    m = max(abs(array))

    # Fonction logistique décalée pour obtenir des valeurs dans l'intervalle [-excentricity; excentricity]
    # Le facteur "6" est utilisé pour restreindre la fonction logistique dans l'intervalle x = [-6, 6]
    normalisation = lambda y: (2 * excentricity / (1 + exp(-6 * y / m))) - excentricity

    # Applique la fonction de normalisation à chaque valeur du tableau
    new_array = np.array([normalisation(y) + value for y in array])
    
    return new_array
