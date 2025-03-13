import numpy as np

def fourier_transform(data, sample_rate, channel_number):
    if channel_number == 2:
        channel_1 = np.mean(data, axis=1) # moyenne car 2 channels
    elif channel_number == 1:
        channel_1 = data
    else:
        raise Exception("Mauvais nombre de Channel")

    # speed-up fft
    fft_length = 2**(int(np.ceil(np.log2(len(channel_1)))))
    channel_1_padded = np.zeros([fft_length])
    channel_1_padded[0:len(channel_1)] = channel_1

    # fourier
    return np.fft.fft(channel_1)