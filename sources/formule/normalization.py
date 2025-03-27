import numpy as np
from math import exp

def normalize_around(array, value, excentricity):
    # Considering the data is centered around 0
    m = max(abs(array))

    # Fonction logistique, décalée pour atteindre des valeurs dans [-excentricity;excentricity]
    # "6" Pour ne garder que le comportement de la fonction logistique de l'intervalle x = [-6,6]
    normalisation = lambda y: (2*excentricity / (1 + exp(-6 * y / m))) - excentricity

    new_array = np.array([normalisation(y) + value for y in array])
    return new_array