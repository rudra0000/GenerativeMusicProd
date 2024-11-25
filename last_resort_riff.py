# import mido
# import random

# # Create a new MIDI file with one track
# midi_file = mido.MidiFile()
# track = mido.MidiTrack()
# midi_file.tracks.append(track)

# # Set the program to electric guitar (or similar instrument)
# track.append(mido.Message('program_change', program=30))  # Program 30: Electric Guitar (clean)

# # Define the simplified riff for "Last Resort" (E minor)
# # We use MIDI notes: E2, G2, B2, A2, C3, etc.
# riff_notes = [
#     40, 43, 47, 45, 48, 47, 43, 40, 45, 43, 40, 47, 43, 45, 48, 43  # E2, G2, B2, A2, C3, ...
# ]

# # Set the rhythm
# duration = 240  # Duration of each note in ticks (this is adjustable)

# # Generate the riff as a repeating pattern
# def generate_riff():
#     for _ in range(4):  # Play the riff 4 times (you can adjust the number of repetitions)
#         for note in riff_notes:
#             track.append(mido.Message('note_on', note=note, velocity=100, time=0))  # Note on
#             track.append(mido.Message('note_off', note=note, velocity=100, time=duration))  # Note off

# # Generate the riff and add it to the track
# generate_riff()

# # Save the MIDI file
# midi_file.save('last_resort_riff.mid')

# print("MIDI file 'last_resort_riff.mid' has been created.")

import mido

# Create a new MIDI file with one track
midi_file = mido.MidiFile()
track = mido.MidiTrack()
midi_file.tracks.append(track)

# Set the program to electric guitar (clean tone)
track.append(mido.Message('program_change', program=30))  # Program 30: Electric Guitar (clean)

# Define the simplified riff for "Drive" (C major)
riff_notes = [
    60, 55, 52, 57, 53, 57, 52, 55, 57, 60, 55, 52, 57  # C4, G3, E4, A3, F4, D4, etc.
]

# Set the rhythm (duration of each note in ticks)
duration = 240  # You can adjust the duration to match the feel of the riff
pause_duration = 120  # Shorter pause for rests between notes

# Generate the riff as a repeating pattern
def generate_riff():
    for _ in range(4):  # Play the riff 4 times (you can adjust repetitions)
        for i, note in enumerate(riff_notes):
            if i % 2 == 0:  # Simulate strumming by adding pause between notes
                track.append(mido.Message('note_on', note=note, velocity=100, time=0))  # Note on
                track.append(mido.Message('note_off', note=note, velocity=100, time=duration))  # Note off
            else:
                track.append(mido.Message('note_on', note=note, velocity=100, time=pause_duration))  # Simulate palm-muted rhythm
                track.append(mido.Message('note_off', note=note, velocity=100, time=duration))  # Note off

# Generate the riff and add it to the track
generate_riff()

# Save the MIDI file
midi_file.save('drive_riff.mid')

print("MIDI file 'drive_riff.mid' has been created.")
