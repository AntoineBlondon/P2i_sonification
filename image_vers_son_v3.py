# -*- coding: utf-8 -*-
"""
Created on Fri Apr 18 10:42:46 2025

@author: pauli

"""
from PIL import Image
from mido import Message, MidiFile, MidiTrack
import math

INSTRUMENTS = {
    "bass": 32,      # Acoustic Bass
    "piano": 0,      # Acoustic Grand Piano
    "violin": 40     # Violin
}

# Note : une couleur donnera une note MIDI (0–127)
def color_to_note(r, g, b):
    brightness = (r + g + b) / 3
    return int(20 + (brightness / 255) * 80)  # notes MIDI de 20 à 100

# Choix de l'instrument en fonction de la fréquence (dérivée de la couleur)
def color_to_instrument(r, g, b):
    brightness = (r + g + b) / 3
    freq = 200 + brightness * (1000 / 255)
    if freq < 400:
        return INSTRUMENTS["bass"]
    elif freq < 800:
        return INSTRUMENTS["piano"]
    else:
        return INSTRUMENTS["violin"]

def sonifier(image):

    # Charger et redimensionner l'image
    img = image.convert("RGB")
    img = img.resize((50, 50))  # Taille raisonnable pour éviter un MIDI trop long

    # Initialisation du fichier MIDI
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    # Instruments par gamme de fréquence
    # (General MIDI Program Numbers : https://www.midi.org/specifications-old/item/gm-level-1-sound-set)


    # Lecture des pixels et génération des notes
    time = 0
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = img.getpixel((x, y))
            note = color_to_note(r, g, b)
            instrument = color_to_instrument(r, g, b)

            # Programme Change (change d’instrument)
            track.append(Message('program_change', program=instrument, time=time))

            # Note ON
            track.append(Message('note_on', note=note, velocity=64, time=0))
            # Note OFF après un petit temps (simule une courte note)
            track.append(Message('note_off', note=note, velocity=64, time=60))

            time = 10  # Espacement entre les notes


    # Sauvegarde
    mid.save("image_musique.mid")
