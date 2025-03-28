#Projet : SpiroLab
#Auteurs : Lamiss Elhbishy, Thomas Diot, Pierre Gallois, Jules Charlier, Jim Garnier

import os
import wave
import numpy as np

app_temp_path = os.getenv("FLET_APP_STORAGE_TEMP")
input_path = os.path.join(app_temp_path, "input.wav")

def input_sound_start(audio_rec):
    print("Enregistrement commencé")
    audio_rec.start_recording(input_path)

def input_sound_end(audio_rec):
    print("Fin de l'enregistrement")
    audio_rec.stop_recording()
    return input_path

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

        # Numpy array à partir des octets
        audio_array = np.frombuffer(data, dtype=np_dtype)

        if sample_width == 1:
            audio_array = audio_array.astype(np.float32) - 128
        elif sample_width == 2 or sample_width == 4:
            audio_array = audio_array.astype(np.float32)

        average = sum(audio_array) / len(audio_array)

        # Division du signal en les 5 parties, une pour chaque paramètre
        nb_paquets = len(audio_array)//5

        paquets = np.array_split(audio_array[0:5*nb_paquets], nb_paquets) # Paquets de 5 valeurs, avec fix pour avoir exactement un multiple de 5 valeurs
        arrays = np.column_stack(paquets)

        return arrays