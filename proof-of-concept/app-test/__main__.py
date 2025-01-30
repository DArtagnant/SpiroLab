#!/usr/bin/python3

if not __package__ == "app-test":
    raise ImportError("Le code doit être appelé en tant que module : `python -m app-test`")

from . import formule
from matplotlib import pyplot as plt
import numpy as np
from . import audio
from . import gui

file_info = audio.test_audio()
fourier = formule.fourier_transform(*file_info)


# plot
w = np.linspace(0, file_info[1], len(fourier)//2)

# First half is the real component, second half is imaginary ┑(￣Д ￣)┍
fourier_to_plot = fourier[0:len(fourier)//2]

plt.figure(1)
plt.plot(w, np.abs(fourier_to_plot))
plt.xlabel('frequency')
plt.ylabel('amplitude')
plt.show()

gui.run_test()













































































#                       LE JS C'EST UN GROS BANGER !!!!! ☆*: .｡. o(≧▽≦)o .｡.:*☆