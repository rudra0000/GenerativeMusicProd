import rashford
import mido

FILENAME='./duckandrun.mid'
# FILENAME='alone.mid'
midi_data=mido.MidiFile(filename=f'./midi_files/{FILENAME}')

midi_track0 = midi_data.tracks[0]
tempo = 0
time_signature = {"numerator": 0, "denominator": 0, "clocks_per_click": 24, "notated_32nd_notes_per_beat": 8}
for x in midi_track0:
    if x.is_meta:
        print(x)
        print(x.type)
        if x.type == 'time_signature':
            time_signature
    # pass



