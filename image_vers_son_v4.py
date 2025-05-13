
from PIL import Image
from mido import Message, MidiFile, MidiTrack
import numpy
from traitement import contour
Dt = 500

def add_chord_to_track(track, chord):
    for note in chord:
        track.append(Message('note_on', note=note, velocity=64, time=0))
    for i, note in enumerate(chord):
        first = chord[0]
        track.append(Message('note_off', note=first, velocity=64, time=Dt))

        for n in chord[1:]:
            track.append(Message('note_off', note=n, velocity=64, time=0))


def find_note(position):
    min, max = 40, 70
    #return int(20 + ((position+1) / 50) * 80) 
    return int(min + ((position+1) / 50) * (max-min)) 


def sonifier(image):

    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    track.append(Message('program_change', program=0, time=0))
    image = image.resize((50, 50))  # Taille raisonnable pour éviter un MIDI trop long
    img = contour(numpy.asarray(image) > 50)
    time=0
    for y in numpy.transpose(img):
        chord = []
        for i, x in enumerate(reversed(y)):
            if x > 0:
                note =  find_note(i)
                chord.append(note)
        add_chord_to_track(track, chord)

    mid.save("image_musique.mid")