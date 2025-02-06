from soundfile import read
from importlib.resources import open_binary

def from_file(obj):
    return read(obj)

def test_audio():
    """
    Renvoie (data, sample_rate, channel_number)
    """
    return *from_file(open_binary("static_data", "test_audio.wav")), 2