#!/usr/bin/python3

if not __package__ == "src":
    raise ImportError("Le code doit être appelé en tant que module : `python -m src`")

from . import formule
from matplotlib import pyplot as plt
import numpy as np
from . import audio

sample_rate, data = audio.test_audio()

# speed-up fft
channel_1 = np.zeros([2**(int(np.ceil(np.log2(len(data))))), 1])
channel_1[0:len(data)] = data
fourier = np.fft.fft(channel_1)

# plot

fourier = np.fft.fft(channel_1)

w = np.linspace(0, 44000, len(fourier))

# First half is the real component, second half is imaginary
fourier_to_plot = fourier[0:len(fourier)//2]
w = w[0:len(fourier)//2]

plt.figure(1)

plt.plot(w, fourier_to_plot)
plt.xlabel('frequency')
plt.ylabel('amplitude')
plt.show()