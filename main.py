import rashford
import mido
import mutator

FILENAME='./duckandrun.mid'
# FILENAME='alone.mid'
midi_data=mido.MidiFile(filename=f'./midi_files/{FILENAME}')

midi_track0 = midi_data.tracks[0]



midi_track1 = midi_data.tracks[1]
tempo = 0
time_signature = {"numerator": 0, "denominator": 0, "clocks_per_click": 24, "notated_32nd_notes_per_beat": 8}
for x in midi_track0:
    if x.is_meta:
        if x.type == 'time_signature':
            time_signature
    # pass

new_song = []
for i in midi_data.tracks:
    midi_track1 = i
    if (midi_track1 == midi_track0):
        continue
    desired_track =  rashford.conv_from_midi(midi_track1)
    mutated_track = mutator.start_time_mutator(desired_track, 5, 0.1)
    mutated_track = mutator.pitch_mutator(mutated_track, 5, 0.1)
    for line in mutated_track:
        rashford.fwrite(line.__str__(), './debug_files/mutated_track.txt')
    midi_track1 = rashford.conv_to_midi(mutated_track)
    new_song.append(midi_track1)
  
rashford.save_track_to_midi(new_song, './test.mid',init_track=midi_track0)


