import random
import format_conversion
import mutator
import crossover
import Final_Rater
import mido
import os
import shutil

def Mutate(track, mutation_rate):
    """
    Apply mutations to the track with the specified mutation rate.
    """
    mutated_track = mutator.actual_time_mutator(track, 5, mutation_rate)
    mutated_track = mutator.pitch_mutator(mutated_track, 5, mutation_rate)
    mutated_track = mutator.simplify_mutator(mutated_track, 5, mutation_rate)
    return mutated_track

def Crossover(track1, track2, iterations):
    """
    Apply crossover to two tracks for the specified number of iterations.
    """
    new1, new2 = track1, track2
    for _ in range(iterations):
        new1, new2 = crossover.crossover_tracks_random(new1, new2)
    return new1, new2

def rate_a_song(file):
    """
    Rate a song using the Final_Rater module.
    """
    rating = Final_Rater.rate_a_song(file)
    return rating['Final Rating']

def generate_population(tracks, population_size=10, mutation_rate=0.3):
    """
    Generate a population of tracks using genetic algorithms.
    """
    population = []

    # Ensure tracks is a list of lists
    if not isinstance(tracks[0], list):
        tracks = [tracks]

    while len(population) < population_size:
        parent1 = random.choice(tracks)
        parent2 = random.choice(tracks)

        # Apply crossover to generate new tracks
        child1, child2 = Crossover(parent1, parent2, iterations=random.randint(1, 5))

        # Apply mutation
        child1 = Mutate(child1, mutation_rate)
        child2 = Mutate(child2, mutation_rate)

        # Add to population
        population.append(child1)
        if len(population) < population_size:
            population.append(child2)

    return population

def delete_output_files_directory(directory_path):
    """
    Deletes the specified directory and all its contents.
    """
    if os.path.exists(directory_path) and os.path.isdir(directory_path):
        shutil.rmtree(directory_path)
        print(f"Deleted directory: {directory_path}")
    else:
        print(f"Directory not found: {directory_path}")

def genetic_algorithm(
    input_song_path, 
    population_size=50, 
    generations=10, 
    initial_mutation_rate=0.5, 
    crossover_rate=0.30, 
    retain_top=3,
    output_dir="./output_files/",
    midi_track0=None
):
    """
    Genetic algorithm to evolve a new song from an input MIDI file.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Step 1: Read the input song
    input_song = mido.MidiFile(input_song_path)
    tracks = input_song.tracks
    track = format_conversion.conv_from_midi(tracks[2])

    if not isinstance(track[0], list):
        track = [track]

    # Step 2: Generate the initial population
    population = generate_population(track, population_size, initial_mutation_rate)

    for gen in range(generations):
        print(f"Generation {gen + 1}/{generations}...")

        # Dynamically adjust the mutation rate
        mutation_rate = initial_mutation_rate * (1 - gen / generations)

        # Step 3: Rate each track in the population
        scored_population = []
        for i, track in enumerate(population):
            temp_file = f"{output_dir}temp_gen{gen}_track{i}.mid"
            track = format_conversion.conv_to_midi(track)
            format_conversion.save_track_to_midi(track, temp_file, init_track=midi_track0)
            score = rate_a_song(temp_file)
            scored_population.append((track, score))

        # Sort population by score
        scored_population.sort(key=lambda x: x[1], reverse=True)
        print(f"Top score in generation {gen + 1}: {scored_population[0][1]}")

        # Retain top performers
        top_tracks = [format_conversion.conv_from_midi(track) for track, score in scored_population[:retain_top]]

        # Generate the next generation
        next_generation = top_tracks[:]
        while len(next_generation) < population_size:
            crossover_iterations = random.randint(1, 5)
            parent1 = random.choice(top_tracks)
            parent2 = random.choice(top_tracks)

            # Apply crossover
            if random.random() < crossover_rate:
                child1, child2 = Crossover(parent1, parent2, crossover_iterations)
            else:
                child1, child2 = parent1, parent2

            # Apply mutation
            child1 = Mutate(child1, mutation_rate)
            child2 = Mutate(child2, mutation_rate)

            # Add children to the next generation
            next_generation.append(child1)
            if len(next_generation) < population_size:
                next_generation.append(child2)

        # Update population
        population = next_generation

    # Step 7: Save and return the best track from the final generation
    best_track = scored_population[0][0]
    best_track_path = os.path.join(output_dir, f"best_track_gen{generations}.mid")
    print(f"Best track score: {scored_population[0][1]}")
    delete_output_files_directory(output_dir)
    return best_track

from mido import MidiFile, MidiTrack

# def save_modified_midi(input_song_path, modified_track, output_song_path):
#     """
#     Save the modified MIDI file, retaining the original tracks except for the modified one.
#     """
#     midi_data = MidiFile(input_song_path)
#     new_midi = MidiFile()

#     for i, track in enumerate(midi_data.tracks):
#         if i == 1:
#             new_midi.tracks.append(modified_track)
#         else:
#             new_midi.tracks.append(track)

#     new_midi.save(output_song_path)
#     print(f"Modified MIDI file saved to: {output_song_path}")
def save_modified_midi(input_song_path, modified_track, output_song_path):
    """
    Save the modified MIDI file, retaining all original tracks except the modified one.
    """
    midi_data = MidiFile(input_song_path)
    new_midi = MidiFile()

    for i, track in enumerate(midi_data.tracks):
        if i == 2:  # Replace only the second track (index 1) with the modified track
            new_midi.tracks.append(MidiTrack(modified_track))
        else:
            new_midi.tracks.append(track)  # Retain other tracks as is

    new_midi1 = MidiFile()
    for i, track in enumerate(midi_data.tracks):
        new_midi1.tracks.append(track)


    new_midi.save(output_song_path)
    new_midi1.save('./midi_files/old.mid')
    print(f"Modified MIDI file saved to: {output_song_path}")


# Example Usage
input_song_path = "./midi_files/alone_fixed.mid"
output_song_path = "./midi_files/evolved.mid"
midi_data = mido.MidiFile(input_song_path)
midi_track0 = midi_data.tracks[0]
modified_track = genetic_algorithm(input_song_path, midi_track0=midi_track0)
save_modified_midi(input_song_path, modified_track, output_song_path)
