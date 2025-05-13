import pretty_midi
import numpy as np
from scipy.io.wavfile import write

# 1) load your MIDI
pm = pretty_midi.PrettyMIDI('image_musique.mid')

# 2) synthesize with a simple sine‐wave timbre
#    (you can pass wave=np.sin explicitly if you like)

# define a sawtooth generator on an array of angles (in radians)
def sawtooth(ang):
    # normalize to [–π,π), then linear ramp from –1 to +1
    return 2*((ang + np.pi) / (2*np.pi) % 1) - 1

# synthesize at 44.1 kHz using that sawtooth
audio = pm.synthesize(fs=44100, wave=sawtooth)

# normalize + write out
audio = audio / np.max(np.abs(audio))
pcm = (audio * 32767).astype(np.int16)
write('output_saw.wav', 44100, pcm)


# 3) normalize to int16 PCM
audio = audio / np.max(np.abs(audio))
pcm   = (audio * 32767).astype(np.int16)

# 4) write out a .wav
write('output.wav', 44100, pcm)
print("Wrote output.wav (%.2f s)" % (len(pcm)/44100))
