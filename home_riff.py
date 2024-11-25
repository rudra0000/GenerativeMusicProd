import mido
import random
import time

# Create a new MIDI file with one track
midi_file = mido.MidiFile()
track = mido.MidiTrack()
midi_file.tracks.append(track)

# Add a MIDI header
track.append(mido.Message('program_change', program=5))  # Set an instrument, e.g., Acoustic Grand Piano

# Set up some parameters
min_note = 60  # MIDI note number for Middle C (C4)
max_note = 72  # MIDI note number for one octave higher (C5)
duration_range = (200, 800)  # Duration in ticks for each note
num_notes = 50  # Total number of notes to generate

# Function to generate random notes

notes = ['60', '63', '60', '65', '60', '67', '60', '68', '70', '72', '60', '63', '60', '65', '60', '67', '60', '68', '70', '72']
durations = [400, 400, 200, 400, 200, 400, 200, 400, 400, 200, 400, 400, 200, 400, 200, 400, 200, 400, 400, 200]
num_notes = len(notes)
def generate_random_notes():
    for i in range(num_notes):
        # note = random.randint(min_note, max_note)  # Random note within range
        note = int(notes[i])
        velocity = 100  # Random velocity (how loud the note is)
        duration = durations[i]  # Random duration of note in ticks
        
        # Note on
        track.append(mido.Message('note_on', note=note, velocity=velocity, time=0))
        
        # Note off after a random duration
        track.append(mido.Message('note_off', note=note, velocity=velocity, time=duration))

# Generate the random notes and add them to the track
generate_random_notes()

# Save the MIDI file
midi_file.save('home_riff.mid')

print("MIDI file 'random_notes.mid' has been created.")
