from PIL import Image
from mido import Message, MidiFile, MidiTrack
import numpy as np
import pretty_midi
from scipy.io.wavfile import write
from traitement import contour, fermeture, apply_threshold
import matplotlib.pyplot as plt




Dt = 50





def piano_wave(phase: np.ndarray) -> np.ndarray:
    """Génère un son de piano par synthèse additive d'harmoniques

    Cette fonction somme un ensemble prédéfini d'harmoniques (partielles)
    pour des angle de phase donnés, puis normalise le résultat entre -1 et 1


    Args:
        phase (np.ndarray):
            Liste des valeurs de phase (en radians)

    Returns:
        np.ndarray:
            Liste des valeurs d'amplitudes synthétisées (normalisées entre [-1, 1])
    """
    PARTIAL_AMPS = [1.00, 0.60, 0.40, 0.25, 0.16, 0.10, 0.06, 0.04]
    sig = sum(amp * np.sin((i+1)*phase)
              for i, amp in enumerate(PARTIAL_AMPS))
    return sig / np.max(np.abs(sig))

def to_piano_wav(midi_path, wav_path, fs=44100):
    """Convertit un fichier MIDI en un fichier WAV en utilisant la synthèse de son de piano

    Args:
        midi_path (str):
            Chemin du fichier MIDI d'entrée
        wav_path (str):
            Chemin de sortie du fichier WAV
        fs (int, optional):
            Fréquence d'échantillonnage (en Hz) (la valeur par défaut et 44100 Hz)

    Returns:
        None
    """
    pm = pretty_midi.PrettyMIDI(midi_path)

    for inst in pm.instruments:
        if not inst.is_drum:
            inst.program = pretty_midi.instrument_name_to_program('Acoustic Grand Piano')

    audio = pm.synthesize(
        fs=fs,
        wave=piano_wave
    )


    audio = audio / np.max(np.abs(audio))
    pcm   = (audio * 32767).astype(np.int16)
    write(wav_path, fs, pcm)
    print(f'Wrote {wav_path} ({len(pcm)/fs:.2f}s)')




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
    min_note, max_note = 40, 70


    value = min_note + ((position + 1) / 50) * (max_note - min_note)


    return int(value)

def sonifier(image, show=False, output_name='image_musique.mid'):
    """Transforme une image en fichier MIDI

    Args:
        image (PIL.Image): L'image a sonifier
        show (bool, optional): Si True, affiche l'image et ses différentes transformations avec matplotlib. (Le défaut est False)
        output_name (str, optional): Le nom du fichier MIDI à générer (Le défaut est 'image_musique.mid')
    """

    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    track.append(Message('program_change', program=0, time=0))

    img = fermeture(contour(apply_threshold(np.asarray(image))), 5)
    img = Image.fromarray(img).resize((100, 70))
    img = apply_threshold(np.asarray(img))

    if show: plt.figure()
    if show: plt.imshow(img, cmap="gray")
    if show: plt.show()
    
    for y in np.transpose(img):
        chord = [ find_note(i)
                  for i, x in enumerate(reversed(y)) 
                  if x>0 ]
        add_chord_to_track(track, chord, Dt)

    mid.save(output_name)