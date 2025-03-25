import os
import wave
import numpy as np
from flet_audio_recorder import AudioRecorderStateChangeEvent, AudioRecorderState, AudioRecorder, AudioEncoder

app_temp_path = os.getenv("FLET_APP_STORAGE_TEMP")
input_path = os.path.join(app_temp_path, "input.wav")

# Enregistement du son
audio_rec = AudioRecorder(
    audio_encoder=AudioEncoder.WAV,
)

def input_sound_start(e):
    print("Enregistrement commencé")
    audio_rec.start_recording(input_path)
def input_sound_end(e):
    print("Fin de l'enregistrement")
    audio_rec.stop_recording()

def read_wav(path):
    data = []

    with wave.open(path, "rb") as file:
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

        if sample_width == 1:
            audio_array = audio_array.astype(np.float32) - 128
        elif sample_width == 2 or sample_width == 4:
            audio_array = audio_array.astype(np.float32)

        average = sum(audio_array) / len(audio_array)

        # Normalisation (préalable) à la moyenne : ne change rien à l'output final car juste un scaling, mais TODO pour retirer et vérifier que ça fonctionne comme prévu
        float_array = audio_array / average


        # Shuffle pour éviter la bizarre behaviour du début
        # TODO++
        np.random.shuffle(float_array)
        # Division du signal en les 5 parties, une pour chaque paramètre
        nb_paquets = len(float_array)//5

        paquets = np.array_split(float_array[0:5*nb_paquets], nb_paquets) # Paquets de 5 valeurs, avec fix pour avoir exactement un multiple de 5 valeurs
        arrays = np.column_stack(paquets)

        return arrays