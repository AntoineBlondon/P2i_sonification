
from PIL import Image
from mido import Message, MidiFile, MidiTrack
import numpy
from traitement import contour, fermeture, ouverture, apply_threshold
import matplotlib.pyplot as plt
Dt = 50

def add_chord_to_track(track, chord, duration=Dt):
    for note in chord:
        track.append(Message('note_on', note=note, velocity=64, time=0))
    for i, note in enumerate(chord):
        track.append(Message('note_off', note=chord[0], velocity=64, time=duration))

    for n in chord[1:]:
        track.append(Message('note_off', note=n, velocity=64, time=0))


def find_note(position):
    min, max = 40, 70
    #return int(20 + ((position+1) / 50) * 80) 
    return int(min + ((position+1) / 50) * (max-min)) 


def sonifier(image, show=False):

    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    track.append(Message('program_change', program=0, time=0))
    img = contour(apply_threshold(numpy.asarray(image)))
    if show: plt.subplot(2,2,1)
    if show: plt.imshow(img, cmap="gray")
    if show: plt.subplot(2,2,2)
    img = fermeture(img, 5)
    if show: plt.imshow(img, cmap="gray")

    img = Image.fromarray(img).resize((100, 70))
    img = apply_threshold(numpy.asarray(img))
    if show: plt.subplot(2,2,3)
    if show: plt.imshow(img, cmap="gray")
    if show: plt.show()
    time=0
    for y in numpy.transpose(img):
        chord = [ find_note(i)
                  for i, x in enumerate(reversed(y)) 
                  if x>0 ]
        add_chord_to_track(track, chord, Dt)

    mid.save("image_musique.mid")