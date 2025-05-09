
from PIL import Image
from mido import Message, MidiFile, MidiTrack
import numpy
from traitement import contour
Dt = 50

def add_chord_to_track(track, chord, time):
    for note in chord:
        track.append(Message('note_on', note=note, velocity=64, time=0))
    for i, note in enumerate(chord):
        track.append(Message('note_off', note=note, velocity=64, time=Dt))



def sonifier(image):

    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    track.append(Message('program_change', program=0, time=0))
    image = image.resize((50, 50))  # Taille raisonnable pour éviter un MIDI trop long
    img = contour(numpy.asarray(image))
    time=0
    for y in numpy.transpose(img):
        chord = []
        for i, x in enumerate(y):
            if x > 0:
                note = int(20 + ((i+1) / 50) * 80) 
                chord.append(note)
        add_chord_to_track(track, chord, time)
        time += Dt

    mid.save("image_musique.mid")