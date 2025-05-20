
from PIL import Image
from mido import Message, MidiFile, MidiTrack
import numpy
from traitement import contour, fermeture, apply_threshold
import matplotlib.pyplot as plt
Dt = 50

def add_chord_to_track(track, chord, duration=Dt):
    """Ajoute un accord à une MidiTrack

    Args:
        track (MidiTrack): La piste sur laquelle ajouter l'accord
        chord (List[int]): L'accord, représenté part une liste de notes à jouer (représentées par leur numéro)
        duration (int, optional): La durée de l'accord. Defaults to Dt.
    """
    if len(chord) == 0:
        track.append(Message('program_change', program=0, time=duration))
    for note in chord:
        track.append(Message('note_on', note=note, velocity=64, time=0))
    for i, note in enumerate(chord):
        track.append(Message('note_off', note=chord[0], velocity=64, time=duration))

    for n in chord[1:]:
        track.append(Message('note_off', note=n, velocity=64, time=0))



def find_note(position, major=False):
    """Renvoie le numero de la note correspondant à la position dans l'image

    Args:
        position (int): La ligne de la note
        major (bool, optional): Si True, on transforme les notes pour qu'elles restent sur la gamme du Do Majeur. Defaults to False.

    Returns:
        int: Le numéro de la note
    """
    
    C_MAJOR_OFFSETS = [0, 2, 4, 5, 7, 9, 11]
    min_note, max_note = 40, 70

    
    # 1) continuous mapping
    value = min_note + ((position + 1) / 50) * (max_note - min_note)

    if not major:
        return int(value)
    
    octave_start = min_note // 12
    octave_end   = max_note // 12
    candidates = [
        12 * octave + offset
        for octave in range(octave_start, octave_end + 1)
        for offset in C_MAJOR_OFFSETS
        if min_note <= 12 * octave + offset <= max_note
    ]

    # 3) pick the C-major note nearest to our continuous value
    #    (ties broken by the first occurrence)
    return min(candidates, key=lambda n: abs(n - value))



def sonifier(image, show=False, output_name='image_musique.mid'):
    """Transforme une image en fichier MIDI

    Args:
        image (PIL.Image): L'image a sonifier
        show (bool, optional): Si True, affiche l'image et ses différentes transformations avec matplotlib. Defaults to False.
    """

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

    mid.save(output_name)