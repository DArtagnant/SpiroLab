import numpy as np
import matplotlib.pyplot as plt
from importlib.resources import open_binary
import scipy.io.wavfile as wav
from scipy.fft import rfft, rfftfreq
 
# Partition list into chunks
def partition_list(lst, size):
    return [lst[i:i + size] for i in range(0, len(lst), size)]

def test_audio():
    """
    Renvoie (data, sample_rate, channel_number)
    """
    file = wav.read(open_binary("static_data", "amogus.wav"))
    return file[1], file[0], 1

if __name__ == "__main__":
    # Récupère les données de l'audio
    SAMPLE_RATE = test_audio()[1]
    amogus = test_audio()[0]
    chunks = partition_list(amogus, 750)

    '''
    for i in range(100):
        yf2 = rfft(chunks[i])
        xf2 = rfftfreq(len(chunks[i]), 1 / 44100)
        plt.subplot(10, 10, i+1)
        plt.xscale("log")
        plt.yscale("log")
        plt.plot(xf2, np.abs(yf2), 'b', lw=0.1)
    '''

    yf2 = rfft(amogus)
    xf2 = rfftfreq(len(amogus), 1 / 44100)
    plt.plot(xf2, np.abs(yf2), 'b', lw=0.1)

    plt.show()