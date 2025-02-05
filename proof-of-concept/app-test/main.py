#!/usr/bin/python3

# if not __package__ == "app-test":
#     raise ImportError("Le code doit être appelé en tant que module : `python -m app-test`")

import os

os.environ["OPENBLAS_NUM_THREADS"] = "1"


import formule
from matplotlib import pyplot as plt
import numpy as np
import audio
import gui
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

# file_info = audio.test_audio()
# fourier = formule.fourier_transform(*file_info)


# # plot
# w = np.linspace(0, file_info[1], len(fourier)//2)

# # First half is the real component, second half is imaginary ┑(￣Д ￣)┍
# fourier_to_plot = fourier[0:len(fourier)//2]

# plt.figure(1)
# plt.plot(w, np.abs(fourier_to_plot))
# plt.xlabel('frequency')
# plt.ylabel('amplitude')
# plt.show()

gui.render()