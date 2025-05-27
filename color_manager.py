import colorsys
import numpy as np
from PIL import Image
import os
from musique_manager import *
import matplotlib.pyplot as plt

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]




def rgb2hsv(rgb_color):
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
    (min_in, max_in) = in_range
    (min_out, max_out) = out_range

    slope = (max_out - min_out) / (max_in - min_in) # Delta y / Delta x
    origin = min_out - slope * min_in

    return slope * value + origin


def hsv_to_chord(hsv_color: tuple[int, int, int], hue_degree_to_frequency: dict[int, int]) -> int:
    hue_entre_0_et_1 = hsv_color[0]

    hue_in_degrees = int(linear_range_mapping(hue_entre_0_et_1, (0, 1), (0, 360))) % 360

    specific_color = find_nearest(list(hue_degree_to_frequency.keys()), hue_in_degrees)

    return hue_degree_to_frequency.get(specific_color)



#note_col = note(hsv_to_chord(rgb2hsv(rgb_color)), 5, 5, 11025)
#writewavfile('out.wav', note_col, 11025)

#os.system(f"aplay -q out.wav")




def histogramme_couleur(image: Image, show: bool=False) -> dict[int, int]:
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
    notes = []
    for freq, intensity in histogramme_couleurs.items():
        notes.append(note(freq, duree=5, amplitude=10*intensity, fe=11025))

    final_chord = accord(notes)
    writewavfile(output_name, final_chord, 11025)



