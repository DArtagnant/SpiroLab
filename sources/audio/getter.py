#Projet : SpiroLab
#Auteurs : Lamiss Elhbishy, Thomas Diot, Pierre Gallois, Jules Charlier, Jim Garnier

import flet_audio_recorder as far
import os
import wave
import numpy as np

# Chemin vers l'espace de stockage temporaire de l'application
app_temp_path = os.getenv("FLET_APP_STORAGE_TEMP")
input_path = os.path.join(app_temp_path, "input.wav")

def input_sound_start(audio_rec: far.AudioRecorder):
    """
    Démarre l'enregistrement audio à l'aide de l'objet audio_rec.

    Cette fonction démarre l'enregistrement et sauvegarde le fichier audio dans
    le répertoire temporaire spécifié par `input_path`.

    Args:
        audio_rec (far.AudioRecorder): L'objet d'enregistrement audio utilisé
                             pour démarrer l'enregistrement.
    """
    print("Enregistrement commencé")
    audio_rec.start_recording(input_path)

def input_sound_end(audio_rec: far.AudioRecorder) -> str:
    """
    Arrête l'enregistrement audio et retourne le chemin du fichier enregistré.

    Cette fonction arrête l'enregistrement et retourne le chemin du fichier `.wav`
    dans lequel l'audio a été enregistré.

    Args:
        audio_rec (far.AudioRecorder): L'objet d'enregistrement audio utilisé pour
                             arrêter l'enregistrement.

    Returns:
        str: Le chemin vers le fichier `.wav` enregistré.
    """
    print("Fin de l'enregistrement")
    audio_rec.stop_recording()
    return input_path

def read_wav(path: str) -> np.ndarray:
    """
    Lit un fichier audio `.wav` et retourne un tableau NumPy contenant les données audio traitées.

    Cette fonction ouvre le fichier `.wav` spécifié, lit les données brutes, les transforme
    en un tableau NumPy, et les traite pour les ramener dans une gamme appropriée en fonction
    de la largeur de l'échantillon.

    Args:
        path (str): Le chemin du fichier `.wav` à lire.

    Returns:
        numpy.ndarray: Un tableau NumPy 2D contenant les données audio divisées en 5 parties égales.
    
    L'array retourné est une matrice où chaque ligne correspond à une partie du signal audio,
    découpée en 5 segments égaux.
    """
    data = []

    # Ouverture du fichier .wav en mode lecture binaire
    with wave.open(path, "rb") as file:
        nframes = file.getnframes()  # Nombre d'échantillons
        sample_width = file.getsampwidth()  # Largeur des échantillons (en octets)

        # Lecture des données audio brutes
        data = file.readframes(nframes)

        # Déterminer le type de données NumPy en fonction de la largeur de l'échantillon
        if sample_width == 1:
            np_dtype = np.uint8  # 1 octet par échantillon
        elif sample_width == 2:
            np_dtype = np.int16  # 2 octets par échantillon
        elif sample_width == 4:
            np_dtype = np.int32  # 4 octets par échantillon
        else:
            raise ValueError(f"Unsupported sample width: {sample_width}")  # Si la largeur de l'échantillon n'est pas supportée

        # Convertir les données audio brutes en tableau NumPy
        audio_array = np.frombuffer(data, dtype=np_dtype)

        # Normaliser les données en fonction de la largeur de l'échantillon
        if sample_width == 1:
            audio_array = audio_array.astype(np.float32) - 128  # Décalage pour obtenir une gamme de -128 à 127
        elif sample_width == 2 or sample_width == 4:
            audio_array = audio_array.astype(np.float32)  # Convertir directement en float32

        # Calcul de la valeur moyenne des données audio
        average = sum(audio_array) / len(audio_array)

        # Découpe le signal audio en 5 parties égales
        nb_paquets = len(audio_array) // 5  # Nombre de paquets, chaque paquet contenant une partie égale du signal

        # Découpage du signal en paquets de 5 valeurs
        paquets = np.array_split(audio_array[0:5 * nb_paquets], nb_paquets)  # Paquets de 5 échantillons
        arrays = np.column_stack(paquets)  # Empile les paquets pour obtenir un tableau 2D

        # Retourne le tableau 2D des paquets audio
        return arrays
