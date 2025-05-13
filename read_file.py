import rtmidi
from mido import MidiFile

# 1) create a JACK‐based MidiOut (using rtapi=…)
midiout = rtmidi.MidiOut(rtapi=rtmidi.API_UNIX_JACK)
midiout.open_virtual_port("Sonification")

# 2) load your .mid file
mid = MidiFile('image_musique.mid')

# 3) send them straight to JACK
for msg in mid.play():
    midiout.send_message(msg.bytes())
