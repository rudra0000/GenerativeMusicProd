import mido

# Load the original MIDI file (for example, 'finalcountdown.mid')
cv1 = mido.MidiFile('finalcountdown.mid', clip=True)

# Select the track you want to isolate (for example, track 0)
source_track = cv1.tracks[2]
print('source trtack len', len(source_track))
print('source trtac',(source_track))

# Create a new MIDI file and a new track
new_mid = mido.MidiFile()
new_track = mido.MidiTrack()

# Optional: Add some meta messages for tempo, key signature, etc.
new_track.append(mido.MetaMessage('key_signature', key='C'))
new_track.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(40)))
new_track.append(mido.MetaMessage('time_signature', numerator=6, denominator=8))

# Copy the events from the source track to the new track
for msg in source_track:
    # We only append musical or relevant events, skipping others like SysEx, etc.
    if not msg.is_meta and msg.type != 'end_of_track':
        print('-----', type(msg))
        print('------------', msg)
        if msg.type == 'note_on' or msg.type == 'note_off':
            msg = mido.Message('note_on', channel=7, note=msg.note, velocity=msg.velocity, time=msg.time)
            new_track.append(msg)
    else:
        print(msg)

new_track.append(mido.MetaMessage('end_of_track'))

# Append the new track to the new MIDI file
new_mid.tracks.append(new_track)

# Save the new MIDI file with the isolated track and added notes
new_mid.save('isolated_track_with_notes.mid')

print("Isolated track with added notes saved to 'isolated_track_with_notes.mid'")

