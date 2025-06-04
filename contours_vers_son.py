from PIL import Image
from mido import Message, MidiFile, MidiTrack
import numpy as np
import pretty_midi
from scipy.io.wavfile import write
from utils_traitement import convertir_en_contour
from couleurs_vers_son import linear_range_mapping
import matplotlib.pyplot as plt




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

def to_piano_wav(midi_path: str, wav_path: str, fs: int=44100) -> None:
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

    audio = pm.synthesize(
        fs=fs,
        wave=piano_wave
    )

    audio = audio / np.max(np.abs(audio))
    pcm   = (audio * 32767).astype(np.int16)
    write(wav_path, fs, pcm)
    print(f'Wrote {wav_path} ({len(pcm)/fs:.2f}s)')




def add_chord_to_track(track: MidiTrack, chord: list[int], duration: int=50) -> None:
    """Ajoute un accord à une MidiTrack

    Args:
        track (MidiTrack): La piste sur laquelle ajouter l'accord
        chord (List[int]): L'accord, représenté part une liste de notes à jouer (représentées par leur numéro)
        duration (int, optional): La durée de l'accord en ms. Defaults to 50 ms.
    """
    if len(chord) == 0:
        track.append(Message('program_change', program=0, time=duration))
    for note in chord:
        track.append(Message('note_on', note=note, velocity=64, time=0))
    for i, note in enumerate(chord):
        track.append(Message('note_off', note=chord[0], velocity=64, time=duration))

    for n in chord[1:]:
        track.append(Message('note_off', note=n, velocity=64, time=0))



def find_note(position: int) -> int:
    """Renvoie le numero de la note correspondant à la position dans l'image, (on fait un mapping linéaire de [0; 70] à [40;82])

    Args:
        position (int): La ligne de la note

    Returns:
        int: Le numéro de la note
    """
    return int(linear_range_mapping(position, (0, 70), (40, 82)))


do_major = np.array([40, 42, 44, 45, 47, 49, 51])

full_notes = np.concatenate((do_major + 12, do_major + 12 * 2, do_major + 12 * 3))


def find_note_do_majeur(position: int) -> int:
    """Renvoie le numero de la note correspondant à la position dans l'image, (on fait un mapping linéaire de [0; 70] à [40;82])

    Args:
        position (int): La ligne de la note

    Returns:
        int: Le numéro de la note
    """
    return full_notes[int(linear_range_mapping(position, (0, 70), (0, len(full_notes)-1)))]



def sonifier(image: Image, show: bool=False, output_name: str='image_musique.mid') -> None:
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

    img = convertir_en_contour(np.asarray(image), 10)

    if show: plt.figure()
    if show: plt.imshow(img, cmap="gray")
    if show: plt.show()

    for y in np.transpose(img):
        chord = [ find_note_do_majeur(i)
                  for i, x in enumerate(reversed(y)) 
                  if x>0 ]
        add_chord_to_track(track, chord, 50)

    mid.save(output_name)