import colorsys
import numpy as np
import PIL
from utils_synthese import *
import matplotlib.pyplot as plt

def find_nearest(array: list | np.ndarray, value: float | int) -> float | int:
    """Trouve la valeur la plus proche dans la liste

    Args:
        array (list | np.ndarray): La liste dans laquelle chercher
        value (float | int): La valeur à chercher

    Returns:
        float | int: La valeur de la liste trouvée
    """
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]




def rgb2hsv(rgb_color: tuple[int, int, int]) -> tuple[float, float, float]:
    """Transforme une couleur RGB en format HSV

    Args:
        rgb_color (tuple[int, int, int]): La couleur en RGB (chaque valeur va de 0 à 255)

    Returns:
        tuple[float, float, float]: La même couleur en format HSV (chaque valeur va de 0 à 1)
    """
    return colorsys.rgb_to_hsv(rgb_color[0] / 255, rgb_color[1] / 255, rgb_color[2] / 255)



hue_degree_to_frequency = {
    0: 174,
    30: 185,
    60: 196,
    90: 208,
    120: 220,
    150: 233,
    180: 246,
    210: 261, 
    240: 277,
    270: 293, 
    300: 311,
    330: 329
}


def linear_range_mapping(value: float, in_range: tuple[float, float], out_range: tuple[float, float]) -> float:
    """Fait un mappage linéaire d'un intervalle à un autre

    Exemple
    >>> linear_range_mapping(20.0, (0.0, 50.0), (0.0, 1.0))
    0.4

    Args:
        value (float): La valeur à mapper
        in_range (tuple[float, float]): L'intervalle d'entrée
        out_range (tuple[float, float]): L'intervalle de sortie

    Returns:
        float: value mappée à l'intervalle de sortie
    """
    (min_in, max_in) = in_range
    (min_out, max_out) = out_range

    slope = (max_out - min_out) / (max_in - min_in) # Delta y / Delta x
    origin = min_out - slope * min_in

    return slope * value + origin


def hsv_to_chord(hsv_color: tuple[float, float, float], hue_degree_to_frequency: dict[int, int]) -> int:
    """Renvoie la fréquence associée à la couleur donnée

    Args:
        hsv_color (tuple[float, float, float]): La couleur en format HSV (chaque valeur va de 0 à 1)
        hue_degree_to_frequency (dict[int, int]): Le dictionnaire qui mappe chaque teinte (en degrées) à chaque fréquence (en Hz)

    Returns:
        int: La fréquence de la couleur donnée
    """
    hue_entre_0_et_1 = hsv_color[0]

    hue_in_degrees = int(linear_range_mapping(hue_entre_0_et_1, (0, 1), (0, 360))) % 360

    specific_color = find_nearest(list(hue_degree_to_frequency.keys()), hue_in_degrees)

    return hue_degree_to_frequency.get(specific_color)



def histogramme_couleur(image: PIL.Image, show: bool=False) -> dict[int, int]:
    """Calcule l'histogramme des couleurs d'une image donnée

    Args:
        image (PIL.Image): L'image RGB à traiter
        show (bool, optional): Si True, plot l'histogramme avec matplotlib. Defaults to False.

    Returns:
        dict[int, int]: L'histogramme des couleurs de l'image
    """
    histogramme_couleurs = {}

    for y in range(image.height):
        for x in range(image.width):
            color = image.getpixel((x, y))
            freq = hsv_to_chord(rgb2hsv(color), hue_degree_to_frequency)
            histogramme_couleurs[freq] = histogramme_couleurs.get(freq, 0) + 1



    maximum = max(histogramme_couleurs.values())
    histogramme_couleurs = {frequency: intensity * 1 / maximum for frequency, intensity in histogramme_couleurs.items()}
    if show: plt.figure()
    if show: plt.bar(histogramme_couleurs.keys(), histogramme_couleurs.values(), 10)
    if show: plt.xticks(sorted(list(hue_degree_to_frequency.values())), ["Rouge", "Orange", "Jaune", "Chartreuse", "Vert", "Printemps", "Cyan", "Azur", "Bleu", "Violet", "Magenta", "Rose"], rotation=45)
    if show: plt.show()
    
    return histogramme_couleurs


def colors_to_wav_file(histogramme_couleurs: dict[int, int], output_name: str='chord.wav') -> None:
    """Transforme un histogramme des couleurs en un fichier WAV

    Args:
        histogramme_couleurs (dict[int, int]): L'histogramme des couleurs associé à une image
        output_name (str, optional): Le nom du fichier à enregistrer. Defaults to 'chord.wav'.
    """
    notes = []
    for freq, intensity in histogramme_couleurs.items():
        notes.append(note(freq, duree=5, amplitude=10*intensity, fe=11025))

    final_chord = accord(notes)
    writewavfile(output_name, final_chord, 11025)



