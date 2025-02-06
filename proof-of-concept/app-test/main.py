#!/usr/bin/python3

# if not __package__ == "app-test":
#     raise ImportError("Le code doit être appelé en tant que module : `python -m app-test`")


import formule
from matplotlib import pyplot as plt
import numpy as np
import gui
import static_data
import os


"""
# Fonctionnel ! Découpe le wav en segments d'une seconde
from pydub import AudioSegment
from pydub.utils import make_chunks

myaudio = AudioSegment.from_file("./app-test/static_data/test_audio.wav" , "wav") 
chunk_length_ms = 1000 # pydub utilise des millisecondes
chunks = make_chunks(myaudio, chunk_length_ms)

# Exportation de tous les segments comme .wav
for i, chunk in enumerate(chunks):
    chunk_name = "./app-test/static_data/chunk{0}.wav".format(i)
    print("exporting", chunk_name)
    chunk.export(chunk_name, format="wav")


# Suppression de tous les segments audio précédemment créés
for i, chunk in enumerate(chunks):
    chunk_name = "./app-test/static_data/chunk{0}.wav".format(i)
    print("removing", chunk_name)
    os.remove(chunk_name)
"""

from soundfile import read
from importlib.resources import open_binary

# Récupère les données de l'audio - La3 440Hz ici
A440 = read(open_binary("static_data", "la3.wav"))[0]
amogus = read(open_binary("static_data", "amogus.wav"))[0]
# Echelle en abscisse pour le tracé
t = [i for i in range(len(amogus))]

# Affichage du signal sonore
plt.plot(t, amogus, 'r', lw=0.1)
plt.show()

# Fourier ist broken
# A440 = formule.fourier_transform(amogus[0], amogus[1], 1)

gui.render()