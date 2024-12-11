import mido
import random

old_file = mido.MidiFile('./midi_files/alone.mid')
new_file = mido.MidiFile()
new_track0 = mido.MidiTrack()
new_file.tracks.append(new_track0)
old_track0 = old_file.tracks[0]

for el in old_track0:
    if el.type != 'set_tempo':
        new_track0.append(el)
    else:
        new_track0.append(mido.MetaMessage('set_tempo', tempo=3000000))
for i in range(1, len(old_file.tracks)):
    old_track = old_file.tracks[i]
    new_track = mido.MidiTrack()
    for el in old_track:
            new_track.append(el)
    new_file.tracks.append(new_track)
new_file.save('./midi_files/alone_fixed.mid')

    
