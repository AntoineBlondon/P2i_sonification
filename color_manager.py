import colorsys
import numpy as np
from PIL import Image
import os
from musique_manager import *

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]


rgb_color = (70, 149, 227)


def rgb2hsv(rgb_color):
    return colorsys.rgb_to_hsv(rgb_color[0] / 255, rgb_color[1] / 255, rgb_color[2] / 255)

def hsv_to_chord(hsv_color):
    notes = [174, 185, 196, 208, 220, 233, 246, 261, 277, 293, 311, 329]

    min, max = 174, 329
    diff = max - min

    step = diff

    return find_nearest(notes, min + diff * hsv_color[0])

print(hsv_to_chord(rgb2hsv(rgb_color)))


#note_col = note(hsv_to_chord(rgb2hsv(rgb_color)), 5, 5, 11025)
#writewavfile('out.wav', note_col, 11025)

#os.system(f"aplay -q out.wav")




a = {

}


image = Image.open('images/autres/bird.jpg').convert("RGB")

for y in range(image.height):
    for x in range(image.width):
        color = image.getpixel((x, y))
        freq = int(hsv_to_chord(rgb2hsv(color)))
        a[freq] = a.get(freq, 0) + 1



maximum = max(a.values())
a = {k: v * 1 / maximum for k, v in a.items()}




print(a)