from scipy.io.wavfile import read

def from_file(path: str):
    return read(path)

def test_audio():
    return from_file("../../test/test_data/test_audio.wav")