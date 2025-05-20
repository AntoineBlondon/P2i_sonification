import numpy as np
import pretty_midi
from scipy.io.wavfile import write

# 1) ADSR envelope generator
def make_adsr(sr, length_s, attack=0.005, decay=0.1, sustain_level=0.6, release=0.2):
    n = int(length_s * sr)
    a = int(attack  * sr)
    d = int(decay   * sr)
    r = int(release * sr)
    s = max(0, n - (a + d + r))
    # attack:     0 → 1
    env_a = np.linspace(0, 1, a,   endpoint=False)
    # decay:      1 → sustain_level
    env_d = np.linspace(1, sustain_level, d, endpoint=False)
    # sustain:    sustain_level flat
    env_s = np.full(s, sustain_level)
    # release:    sustain_level → 0
    env_r = np.linspace(sustain_level, 0, r, endpoint=False)
    env = np.concatenate((env_a, env_d, env_s, env_r))
    # pad or trim to exactly n samples
    if len(env) < n:
        env = np.pad(env, (0, n - len(env)))
    else:
        env = env[:n]
    return env

# 2) a “piano-like” partial series (you can tweak these amplitudes)
PARTIAL_AMPS = [1.00, 0.60, 0.40, 0.25, 0.16, 0.10, 0.06, 0.04]

def synth_note(note, duration_s, velocity, sr):
    """
    Return a numpy array of length duration_s*sr
    containing a weighted sum of sine-partials × ADSR envelope.
    """
    length = int(duration_s * sr)
    t = np.arange(length) / sr
    # fundamental frequency
    f0 = 440.0 * 2 ** ((note - 69) / 12)
    # sum up partials
    wave = sum(amp * np.sin(2 * np.pi * f0 * (i+1) * t)
               for i, amp in enumerate(PARTIAL_AMPS))
    # normalize so partial mix doesn’t clip
    wave = wave / np.max(np.abs(wave))
    # apply velocity (0…1) and envelope
    env = make_adsr(sr, duration_s)
    return wave * env * velocity

def piano_wave(phase: np.ndarray) -> np.ndarray:
    PARTIAL_AMPS = [1.00, 0.60, 0.40, 0.25, 0.16, 0.10, 0.06, 0.04]
    sig = sum(amp * np.sin((i+1)*phase)
              for i, amp in enumerate(PARTIAL_AMPS))
    return sig / np.max(np.abs(sig))

def to_piano_wav(midi_path, wav_path, fs=44100, amplitude=0.2):
    # 2) Load with PrettyMIDI (handles tempo maps, multiple tracks, etc.)
    pm = pretty_midi.PrettyMIDI(midi_path)

    # 3) (Optional) force the GM program to Acoustic Grand Piano
    for inst in pm.instruments:
        if not inst.is_drum:
            inst.program = pretty_midi.instrument_name_to_program('Acoustic Grand Piano')

    # 4) Let PrettyMIDI “synthesize” every note you’ve added,
    #    using your piano_wave + ADSR, and it’ll give you the *full* waveform
    audio = pm.synthesize(
        fs=fs,
        wave=lambda phase: piano_wave(phase),
        # you can’t directly pass an envelope here, so
        # build your ADSR into the wave or post-process each note
    )

    # 5) normalize + write
    audio = audio / np.max(np.abs(audio))
    pcm   = (audio * 32767).astype(np.int16)
    write(wav_path, fs, pcm)
    print(f'Wrote {wav_path} ({len(pcm)/fs:.2f}s)')


if __name__ == '__main__':
    to_piano_wav('image_musique.mid', 'piano_output.wav')
