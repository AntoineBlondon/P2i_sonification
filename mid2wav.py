import numpy as np
import pretty_midi
from scipy.io.wavfile import write


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

    # 5) normalize + write
    audio = audio / np.max(np.abs(audio))
    pcm   = (audio * 32767).astype(np.int16)
    write(wav_path, fs, pcm)
    print(f'Wrote {wav_path} ({len(pcm)/fs:.2f}s)')


if __name__ == '__main__':
    to_piano_wav('image_musique.mid', 'piano_output.wav')
