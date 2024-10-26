import mido
import random
from midiutil import MIDIFile

# Constants
POPULATION_SIZE = 10
MAX_GENERATIONS = 100
MUTATION_RATE = 0.05

def extractNotesFromMidi(file_path):
    """Extracts all unique notes from a MIDI file."""
    midi = mido.MidiFile(file_path)
    notes = set()
    tempo = 120  # Default tempo

    for track in midi.tracks:
        for msg in track:
            if msg.type == 'note_on' and msg.velocity > 0:
                notes.add(msg.note)
            elif msg.type == 'set_tempo':
                tempo = mido.tempo2bpm(msg.tempo)

    return sorted(notes), tempo


def generateGenome(scale):
    """Generates a note sequence (genome)."""
    return [[random.choice(scale) for _ in range(16)] for _ in range(8)]

def generatePopulation(n, scale):
    """Generates a population of melodies."""
    return [generateGenome(scale) for _ in range(n)]


# Fitness functions
def melodicSmoothness(genome):
    flattened_genome = [note for sublist in genome for note in sublist]
    smoothnessScore = sum([abs(flattened_genome[i] - flattened_genome[i-1])**2 for i in range(1, len(flattened_genome))])
    return -smoothnessScore

def rhythmicRegularity(genome):
    rhythm_score = 0
    for measure in genome:
        if measure == genome[0]:
            rhythm_score += 10
        else:
            rhythm_score -= 5
    return rhythm_score

def harmonicCompatibility(genome):
    consonant_intervals = [0, 4, 7, 12]
    harmony_score = 0
    flattened_genome = [note for sublist in genome for note in sublist]
    for i in range(1, len(flattened_genome)):
        interval = abs(flattened_genome[i] - flattened_genome[i-1]) % 12
        if interval in consonant_intervals:
            harmony_score += 10
        else:
            harmony_score -= 5
    return harmony_score

def scaleAdherence(genome, scale):
    adherence_score = 0
    flattened_genome = [note for sublist in genome for note in sublist]
    for note in flattened_genome:
        if note in scale:
            adherence_score += 5
        else:
            adherence_score -= 10
    return adherence_score

# Combined fitness function
def combinedFitnessFunction(genome, scale):
    smoothness = melodicSmoothness(genome)
    rhythm = rhythmicRegularity(genome)
    harmony = harmonicCompatibility(genome)
    scale_adherence = scaleAdherence(genome, scale)
    
    return (smoothness * 0.3 + rhythm * 0.2 + harmony * 0.3 + scale_adherence * 0.2)

def selectParents(population, scale):
    fitness_scores = [combinedFitnessFunction(genome, scale) for genome in population]
    min_fitness = min(fitness_scores)
    
    # Adjust scores if all are zero or negative to ensure they are positive
    if min_fitness <= 0:
        fitness_scores = [score - min_fitness + 1 for score in fitness_scores]  # Shift and ensure no zero weights

    return random.choices(population, k=2, weights=fitness_scores)

def crossoverFunction(parentA, parentB):
    singlePoint = random.randint(1, len(parentA) - 1)
    childA = parentA[:singlePoint] + parentB[singlePoint:]
    childB = parentB[:singlePoint] + parentA[singlePoint:]
    return childA, childB

def mutateGenome(genome, mutationRate, scale):
    for i in range(len(genome)):
        for j in range(len(genome[i])):
            if random.uniform(0, 1) <= mutationRate:
                genome[i][j] = random.choice(scale)
    return genome

def runEvolution(mutationRate, scale):
    population = generatePopulation(POPULATION_SIZE, scale)
    
    for generation in range(MAX_GENERATIONS):
        population = sorted(population, key=lambda genome: combinedFitnessFunction(genome, scale), reverse=True)
        nextGeneration = population[:2]  # Elitism
        
        for _ in range(int(len(population) / 2) - 1):
            parentA, parentB = selectParents(population, scale)
            childA, childB = crossoverFunction(parentA, parentB)
            childA = mutateGenome(childA, mutationRate, scale)
            childB = mutateGenome(childB, mutationRate, scale)
            nextGeneration += [childA, childB]
        
        population = nextGeneration

    best_genome = max(population, key=lambda genome: combinedFitnessFunction(genome, scale))
    return best_genome


def generateBassline(chord_progression, genre):
    bassline = []
    for chord in chord_progression:
        root = chord[0]
        if genre == "jazz":
            bassline.append([root, root + 3, root + 5, root + 7])  # Walking bass
        elif genre == "classical":
            bassline.append([root, root - 12, root + 7, root - 5])  # Root and octave variations
        else:
            bassline.append([root] * 16)  # Repeats root note
    return bassline

def addHarmonyTrack(midiFile, chord_progression, track_num):
    time = 0
    channel = 1
    duration = 2
    volume = 80

    for chord in chord_progression:
        for note in chord:
            midiFile.addNote(track_num, channel, note, time, duration, volume)
        time += 2

def addBasslineTrack(midiFile, bassline, track_num):
    time = 0
    channel = 2
    volume = 100

    for measure in bassline:
        for note in measure:
            duration = 1
            midiFile.addNote(track_num, channel, note, time, duration, volume)
            time += 1

def generateChordProgression(scale, genre):
    """Generates a genre-based chord progression."""
    chords = []
    if genre == "jazz":
        # Jazz progression
        chords = [[scale[0], scale[2], scale[4]], [scale[3], scale[5], scale[7]],
                  [scale[4], scale[6], scale[1]], [scale[2], scale[4], scale[6]]]
    elif genre == "rock":
        # Rock power chords
        chords = [[scale[0], scale[4]], [scale[5], scale[9]], [scale[7], scale[11]], [scale[4], scale[8]]]
    elif genre == "electronic":
        # Progressive house / EDM chord progression
        for _ in range(8):
            root = random.choice(scale[:5])  # Choose a root within the first half of the scale
            chord = [root, root + 3, root + 7]  # Minor triad
            chords.append(chord)
    return chords

def addGenreDrums(midiFile, length, genre):
    """Adds genre-specific drums to the MIDI file."""
    track = 3  # Drum track
    time = 0
    percussion_channel = 9  # Standard percussion channel
    base_volume = 100

    if genre == "jazz":
        # Jazz brush drums or swing pattern
        # [Add jazz-specific drum pattern here]
        pass
    elif genre == "rock":
        # Rock beat with kick and snare
        # [Add rock-specific drum pattern here]
        pass
    elif genre == "electronic":
        # EDM / Progressive House beat
        kick = 36  # Bass drum
        snare = 38  # Snare drum
        hi_hat_closed = 42  # Closed hi-hat

        for i in range(length):
            # Four-on-the-floor kick pattern
            if i % 4 == 0:
                midiFile.addNote(track, percussion_channel, kick, time, 1, base_volume)
            # Snare on beats 2 and 4
            if i % 4 == 2:
                midiFile.addNote(track, percussion_channel, snare, time, 1, base_volume - 20)
            # Closed hi-hat on every beat
            midiFile.addNote(track, percussion_channel, hi_hat_closed, time, 1, base_volume - 30)

            time += 1

def writeMidiToDisk(sequence, chord_progression, bassline, filename="output", tempo=120, genre="classical"):
    time = 0
    midiFile = MIDIFile(4)
    midiFile.addTempo(0, time, tempo)

    flattened_sequence = [note for sublist in sequence for note in sublist]
    for i, pitch in enumerate(flattened_sequence):
        duration = random.choice([0.5, 0.75, 1])
        if pitch is not None:
            midiFile.addNote(0, 0, pitch, time, duration, 100)
        time += 1

    addHarmonyTrack(midiFile, chord_progression, 1)
    addBasslineTrack(midiFile, bassline, 2)
    addGenreDrums(midiFile, len(flattened_sequence), genre)

    with open(f"{filename}.mid", "wb") as output_file:
        midiFile.writeFile(output_file)
def writeBasicMidi(sequence, filename="basic_output"):
    """Writes a basic MIDI file with just the melody."""
    time = 0
    midiFile = MIDIFile(1)  # Only 1 track for melody
    midiFile.addTempo(0, time, 120)

    flattened_sequence = [note for sublist in sequence for note in sublist]
    for pitch in flattened_sequence:
        duration = random.choice([0.5, 0.75, 1])
        if pitch is not None:
            midiFile.addNote(0, 0, pitch, time, duration, 100)
        time += 1

    with open(f"{filename}.mid", "wb") as output_file:
        midiFile.writeFile(output_file)


# Usage Example
midi_file_path = './alan_walker_-_alone.mid'
genre = "electronic"

try:
    scale, tempo = extractNotesFromMidi(midi_file_path)
    best_melody = runEvolution(MUTATION_RATE, scale)
    writeBasicMidi(best_melody, filename="generated1232_melody")
    chord_progression = generateChordProgression(scale, genre)
    bassline = generateBassline(chord_progression, genre)

    writeMidiToDisk(best_melody, chord_progression, bassline, filename="generated12342_song", tempo=150, genre=genre)

except Exception as e:
    print(f"An error occurred: {e}")