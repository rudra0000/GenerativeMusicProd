import random
import format_conversion
import mutator
import crossover
import main2
import mido
import os

def Mutate(track, prob_mutation=0.3):
    mutated_track = mutator.actual_time_mutator(track, 5, 0.1)
    mutated_track = mutator.pitch_mutator(mutated_track, 5, 0.1)
    mutated_track = mutator.simplify_mutator(mutated_track, 5, 0.3)
    return mutated_track

def Crossover(track1, track2):
    new1 = track1
    new2 = track2
    for j in range(5):
        new1, new2 = crossover.crossover_tracks_random(new1, new2)
    
    # Print the result after each iteration
    return new1, new2

def rate_a_song(file):
    rating = main2.rate_a_song(file)
    rating = rating['Final Rating']
    return rating

def generate_population(tracks, population_size=10, prob_mutation=0.3):
    """
    Generate a population of tracks using genetic algorithms.
    
    Parameters:
        tracks (list): A list of input tracks. Can contain one or more tracks.
        population_size (int): The number of tracks to generate in the population.
        prob_mutation (float): The probability of applying mutations to the tracks.
    
    Returns:
        list: A list of generated tracks forming the population.
    """
    population = []

    # If only one track is given, duplicate it to use for crossover
    if not isinstance(tracks[0], list):
        tracks = [tracks]
    
    while len(population) < population_size:
        # Randomly pick two parent tracks from the input list
        parent1 = random.choice(tracks)
        parent2 = random.choice(tracks)

        # Apply crossover to generate new tracks
        child1, child2 = parent1, parent2
        child1, child2 = Crossover(child1, child2)

        # Apply mutation with the given probability
        if random.random() < prob_mutation:
            child1 = Mutate(child1, prob_mutation)
        if random.random() < prob_mutation:
            child2 = Mutate(child2, prob_mutation)

        # Add new tracks to the population
        population.append(child1)
        if len(population) < population_size: 
            population.append(child2)
    
    return population

import shutil

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
    generations=2, 
    prob_mutation=0.25, 
    crossover_rate=0.35, 
    retain_top=3,
    output_dir="./output_files/",
    midi_track0=None
):
    """
    Genetic algorithm to evolve a new song from an input MIDI file.

    Parameters:
        input_song_path (str): File path to the input song in .mid format.
        population_size (int): Number of tracks in each generation.
        generations (int): Number of generations to run.
        prob_mutation (float): Probability of mutation.
        crossover_rate (float): Probability of applying crossover.
        retain_top (int): Number of top-rated tracks to retain in each generation.
        output_dir (str): Directory to save evolved tracks.

    Returns:
        str: File path of the best evolved track in .mid format.
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Step 1: Read the input song
    input_song = mido.MidiFile(input_song_path)
    tracks = input_song.tracks
    track = format_conversion.conv_from_midi(tracks[1])

    if not isinstance(track[0], list):
        track = [track]
    # Step 2: Generate the initial population
    population = generate_population(track, population_size, prob_mutation)

    for gen in range(generations):
        print(f"Generation {gen + 1}/{generations}...")

        # Step 3: Rate each track in the population
        scored_population = []
        for i, track in enumerate(population):
            # Save the track as a temporary .mid file to be rated
            temp_file = f"{output_dir}temp_gen{gen}_track{i}.mid"
            track = format_conversion.conv_to_midi(track)
            format_conversion.save_track_to_midi(track, temp_file,init_track=midi_track0)
            score = rate_a_song(temp_file)
            scored_population.append((track, score))

        # Step 4: Sort population by score (higher is better)
        scored_population.sort(key=lambda x: x[1], reverse=True)
        print(f"Top score in generation {gen + 1}: {scored_population[0][1]}")

        # Step 5: Retain top performers
        top_tracks = [format_conversion.conv_from_midi(track) for track, score in scored_population[:retain_top]]

        # Step 6: Generate the next generation
        next_generation = top_tracks[:]
        print(f'len(top_tracks): {type(top_tracks[0])}')
        while len(next_generation) < population_size:
            # Select two parents randomly from the top tracks
            parent1 = random.choice(top_tracks)
            parent2 = random.choice(top_tracks)
            # Apply crossover with probability
            if random.random() < crossover_rate:
                child1, child2 = Crossover(parent1, parent2)
            else:
                child1, child2 = parent1, parent2

            # Apply mutation with probability
            if random.random() < prob_mutation:
                child1 = Mutate(child1, prob_mutation)
            if random.random() < prob_mutation:
                child2 = Mutate(child2, prob_mutation)

            # Add children to the next generation
            next_generation.append(child1)
            if len(next_generation) < population_size:
                next_generation.append(child2)

        # Update population for the next generation
        population = next_generation

    # Step 7: Save and return the best track from the final generation
    best_track = scored_population[0][0]
    best_track_path = os.path.join(output_dir, f"best_track_gen{generations}.mid")
    
    print(f"Best track score: {scored_population[0][1]}")
    delete_output_files_directory(output_dir)
    return best_track

from mido import MidiFile, MidiTrack, Message

def save_modified_midi(input_song_path, modified_track, output_song_path):
    """
    Save the modified MIDI file, retaining the original tracks except for the modified one.
    """
    # Load the original MIDI file
    midi_data = MidiFile(input_song_path)
    
    # Create a new MIDI file to save the result
    new_midi = MidiFile()

    # Replace track 0 with the modified track, and copy other tracks as is
    for i, track in enumerate(midi_data.tracks):
        if i == 1:  # Assuming track[0] is modified
            new_midi.tracks.append(modified_track)
        else:
            if i == 0:
                new_track = MidiTrack()
                new_track.append(mido.MetaMessage('set_tempo', tempo=1000000))
                new_midi.tracks.append(new_track)
            else:
                new_midi.tracks.append(track)

    # Save the new MIDI file
    new_midi.save(output_song_path)
    print(f"Modified MIDI file saved to: {output_song_path}")


# Run the genetic algorithm on an example input song
# input_song_path = "./midi_files/alone_fixed.mid"
# midi_data = mido.MidiFile(input_song_path)
# midi_track0 = midi_data.tracks[0]
# track1 =  genetic_algorithm(input_song_path,midi_track0=midi_track0)
# baby, 
input_song_path = "./midi_files/pirates.mid"
output_song_path = "./midi_files/evolved_song.mid"

# Step 1: Load the original MIDI file
midi_data = mido.MidiFile(input_song_path)

# Step 2: Extract the first track (or the track you want to modify)
midi_track0 = midi_data.tracks[0]

# Step 3: Run the genetic algorithm to generate a new track
modified_track = genetic_algorithm(input_song_path, midi_track0=midi_track0)

# Step 4: Save the new MIDI file with the modified track
save_modified_midi(input_song_path, modified_track, output_song_path)
