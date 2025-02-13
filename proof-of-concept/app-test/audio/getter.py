import numpy as np
import matplotlib.pyplot as plt
from soundfile import read
from importlib.resources import open_binary

# Récupère les données de l'audio - La3 440Hz ici
A440 = read(open_binary("static_data", "la3.wav"))[0]
amogus = read(open_binary("static_data", "amogus.wav"))[0]
# Echelle en abscisse pour le tracé
t1 = [i for i in range(len(A440))]
t2 = [i for i in range(len(amogus))]
A440_fft = np.fft.fft(A440)
x = [i for i in range(len(A440_fft))]

# Affichage du signal sonore
plt.subplot(2, 2, 1)
plt.plot(t1, A440, 'r', lw=0.1)
plt.subplot(2, 2, 2)
plt.plot(t2, amogus, 'r', lw=0.1)
plt.subplot(2, 2, 3)
plt.plot(x, A440_fft, 'r', lw=0.1)
plt.show()

# Fourier ist broken
# A440 = formule.fourier_transform(amogus[0], amogus[1], 1)

def from_file(obj):
    return read(obj)

def test_audio():
    """
    Renvoie (data, sample_rate, channel_number)
    """
    return *from_file(open_binary("static_data", "amogus.wav")), 1