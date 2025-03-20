import os
import wave
import numpy as np
from flet_audio_recorder import AudioRecorderStateChangeEvent, AudioRecorderState, AudioRecorder, AudioEncoder

app_temp_path = os.getenv("FLET_APP_STORAGE_TEMP")
input_path = os.path.join(app_temp_path, "input.wav")
print(app_temp_path, input_path)

# Enregistement du son
audio_rec = AudioRecorder(
    audio_encoder=AudioEncoder.WAV,
)

def input_sound_start(e):
    print("Enregistrement commencé")
    audio_rec.start_recording(input_path)
def input_sound_end(e):
    print("Fin de l'enrgeistrement")
    audio_rec.stop_recording()


def read_wav():
    data = []

    with wave.open(input_path, "rb") as file:
        nframes = file.getnframes()
        sample_width = file.getsampwidth()

        data = file.readframes(nframes)

        if sample_width == 1:
            np_dtype = np.uint8
        elif sample_width == 2:
            np_dtype = np.int16
        elif sample_width == 4:
            np_dtype = np.int32
        else:
            raise ValueError(f"Unsupported sample width: {sample_width}")

        # Numpy array à partir des bytes
        audio_array = np.frombuffer(data, dtype=np_dtype)

        # Normalisation à la moyenne
        if sample_width == 1:
            audio_array = audio_array.astype(np.float32) - 128
        elif sample_width == 2 or sample_width == 4:
            audio_array = audio_array.astype(np.float32)

        average = sum(audio_array) / len(audio_array)

        float_array = audio_array / average
        return np.array_split(float_array, len(float_array)//5)