import rashford
import mido
import mutator
import raters

# FILENAME='./midi_files/duckandrun.mid'
# FILENAME='./midi_files/whenimgone.mid'


# any song's crazy rating is the song's first track's crazy rating

rating_dict = {} # maps the song's name to its a dictionary of its ratings

best_files =['./midi_files/pain_riff.mid','./midi_files/loser.mid']
crazy_ratings_sum = 0
direction_of_melody_sum = 0
direction_stability_sum = 0
pitch_range_sum = 0
# scale_rating_sum = 0

# scale_rating_target = 0
# scale_rating_max = 0
pitch_range_max = 0
direction_stability_max = 0
direction_of_melody_max = 0
crazy_rating_max = 0
# scale_rating_min = 0
pitch_range_min = 0
direction_stability_min = 0
direction_of_melody_min = 0
crazy_rating_min = 0
repetition_rating_sum = 0
repetition_rating_max = 0
repetition_rating_min = 0
equal_consecutive_notes_rating_sum = 0
equal_consecutive_notes_rating_max = 0
equal_consecutive_notes_rating_min = 0
unique_rhythm_values_sum = 0
unique_rhythm_values_max = 0
unique_rhythm_values_min = 0
equal_consecutive_notes_rating_target = 0
pitch_range_target = 0
direction_stability_target = 0
direction_of_melody_target = 0
crazy_rating_target = 0
repetition_rating_target = 0
unique_rhythm_values_target = 0

for file in best_files:
    rating_dict[file] = {}

for file in best_files:
    midi_data=mido.MidiFile(filename=f'{file}')
    midi_track0 = midi_data.tracks[0]
    midi_track1 = midi_data.tracks[1]
    midi_track1 = rashford.conv_from_midi(midi_track1)
    rating_dict[file]['crazy_rating'] = raters.neighboring_pitch_range(midi_track1, 12)
    crazy_ratings_sum += rating_dict[file]['crazy_rating']
    rating_dict[file]['direction_of_melody'] = raters.direction_of_melody(midi_track1, 12) 
    direction_of_melody_sum += rating_dict[file]['direction_of_melody']
    rating_dict[file]['direction_stability'] = raters.direction_stability(midi_track1)
    direction_stability_sum += rating_dict[file]['direction_stability']
    rating_dict[file]['pitch_range'] = raters.pitch_range(midi_track1)
    rating_dict[file]['repetition_rating'] = raters.repetition_rating(midi_track1)
    repetition_rating_sum += rating_dict[file]['repetition_rating']
    rating_dict[file]['equal_consecutive_notes_rating'] = raters.equal_consecutive_notes(midi_track1)
    equal_consecutive_notes_rating_sum += rating_dict[file]['equal_consecutive_notes_rating']
    rating_dict[file]['unique_rhythm_values'] = raters.unique_rhythm_values(midi_track1)
    unique_rhythm_values_sum += rating_dict[file]['unique_rhythm_values']


    pitch_range_sum += rating_dict[file]['pitch_range']
    print(f'crazy_rating: {rating_dict[file]["crazy_rating"]}')
    print(f'direction_of_melody: {rating_dict[file]["direction_of_melody"]}')
    print(f'direction_stability: {rating_dict[file]["direction_stability"]}')
    print(f'pitch_range: {rating_dict[file]["pitch_range"]}')
    print(f'repetition_rating: {rating_dict[file]["repetition_rating"]}')
    print(f'equal_consecutive_notes_rating: {rating_dict[file]["equal_consecutive_notes_rating"]}')
    print(f'unique_rhythm_values: {rating_dict[file]["unique_rhythm_values"]}')

    print('###################################################################')
    print('###################################################################')
    # rating_dict[file]['scale_rating'] = raters.calculate_scale_pattern_rating(midi_track1)
    # scale_rating_sum += rating_dict[file]['scale_rating']
    # scale_rating_max = max(scale_rating_max, rating_dict[file]['scale_rating'])
    pitch_range_max = max(pitch_range_max, rating_dict[file]['pitch_range'])
    direction_stability_max = max(direction_stability_max, rating_dict[file]['direction_stability'])
    direction_of_melody_max = max(direction_of_melody_max, rating_dict[file]['direction_of_melody'])
    crazy_rating_max = max(crazy_rating_max, rating_dict[file]['crazy_rating'])
    # scale_rating_min = min(scale_rating_min, rating_dict[file]['scale_rating'])
    pitch_range_min = min(pitch_range_min, rating_dict[file]['pitch_range'])
    direction_stability_min = min(direction_stability_min, rating_dict[file]['direction_stability'])
    direction_of_melody_min = min(direction_of_melody_min, rating_dict[file]['direction_of_melody'])
    crazy_rating_min = min(crazy_rating_min, rating_dict[file]['crazy_rating'])
    repetition_rating_max = max(repetition_rating_max, rating_dict[file]['repetition_rating'])
    repetition_rating_min = min(repetition_rating_min, rating_dict[file]['repetition_rating'])
    equal_consecutive_notes_rating_max = max(equal_consecutive_notes_rating_max, rating_dict[file]['equal_consecutive_notes_rating'])
    equal_consecutive_notes_rating_min = min(equal_consecutive_notes_rating_min, rating_dict[file]['equal_consecutive_notes_rating'])
    unique_rhythm_values_max = max(unique_rhythm_values_max, rating_dict[file]['unique_rhythm_values'])
    unique_rhythm_values_min = min(unique_rhythm_values_min, rating_dict[file]['unique_rhythm_values'])



# scale_rating_target = scale_rating_sum/len(best_files)
pitch_range_target = pitch_range_sum/len(best_files)
direction_stability_target = direction_stability_sum/len(best_files)
direction_of_melody_target = direction_of_melody_sum/len(best_files)
crazy_rating_target = crazy_ratings_sum/len(best_files)

influence = {}
# influence['scale_rating'] = 2*(0.5 - min(scale_rating_target - scale_rating_min,scale_rating_max - scale_rating_target))
influence['pitch_range'] = 2*(0.5 - min(pitch_range_target - pitch_range_min,pitch_range_max - pitch_range_target))
influence['direction_stability'] = 2*(0.5 - min(direction_stability_target - direction_stability_min,direction_stability_max -direction_stability_target))
influence['direction_of_melody'] = 2*(0.5 - min(direction_of_melody_target - direction_of_melody_min,direction_of_melody_max - direction_of_melody_target))
influence['crazy_rating'] = 2*(0.5 - min(crazy_rating_target - crazy_rating_min,crazy_rating_max - crazy_rating_target))
influence['repetition_rating'] = 2*(0.5 - min(repetition_rating_target - repetition_rating_min,repetition_rating_max - repetition_rating_target))
influence['equal_consecutive_notes_rating'] = 2*(0.5 - min(equal_consecutive_notes_rating_target - equal_consecutive_notes_rating_min,equal_consecutive_notes_rating_max - equal_consecutive_notes_rating_target))
influence['unique_rhythm_values'] = 2*(0.5 - min(unique_rhythm_values_target - unique_rhythm_values_min,unique_rhythm_values_max - unique_rhythm_values_target))
influence['pitch_range'] = 1
influence['direction_stability'] = 1
influence['direction_of_melody'] = 1
influence['crazy_rating'] = 1
influence['repetition_rating'] = 1
influence['equal_consecutive_notes_rating'] = 1
influence['unique_rhythm_values'] = 1


# def rate_a_song(file):
#     midi_data=mido.MidiFile(filename=f'{file}')
#     midi_track0 = midi_data.tracks[0]
#     midi_track1 = midi_data.tracks[1]
#     midi_track1 = rashford.conv_from_midi(midi_track1)
#     rating = 0
#     rating += influence['crazy_rating'] * abs(raters.neighboring_pitch_range(midi_track1, 12) - crazy_rating_target)
#     rating += influence['direction_of_melody'] * abs(raters.direction_of_melody(midi_track1, 12) - direction_of_melody_target)
#     rating += influence['direction_stability'] * abs(raters.direction_stability(midi_track1) - direction_stability_target)
#     rating += influence['pitch_range'] * abs(raters.pitch_range(midi_track1) - pitch_range_target)
#     # rating += influence['scale_rating'] * (raters.calculate_scale_pattern_rating(midi_track1) - scale_rating_target)
#     total_influence = influence['crazy_rating'] + influence['direction_of_melody'] + influence['direction_stability'] + influence['pitch_range']
#     rating = rating/total_influence
#     return rating

import pandas as pd  # Import pandas for better table formatting

def rate_a_song(file):
    midi_data = mido.MidiFile(filename=f'{file}')
    midi_track0 = midi_data.tracks[0]
    midi_track1 = midi_data.tracks[1]
    midi_track1 = rashford.conv_from_midi(midi_track1)
    
    # Calculate individual ratings
    crazy_rating = raters.neighboring_pitch_range(midi_track1, 12)
    direction_of_melody = raters.direction_of_melody(midi_track1, 12)
    direction_stability = raters.direction_stability(midi_track1)
    pitch_range = raters.pitch_range(midi_track1)
    repetition_rating = raters.repetition_rating(midi_track1)
    equal_consecutive_notes_rating = raters.equal_consecutive_notes(midi_track1)
    unique_rhythm_values = raters.unique_rhythm_values(midi_track1)
    
    # Calculate weighted rating
    rating = 0
    rating += influence['crazy_rating'] * abs(crazy_rating - crazy_rating_target)
    rating += influence['direction_of_melody'] * abs(direction_of_melody - direction_of_melody_target)
    rating += influence['direction_stability'] * abs(direction_stability - direction_stability_target)
    rating += influence['pitch_range'] * abs(pitch_range - pitch_range_target)
    rating += influence['repetition_rating'] * abs(repetition_rating - repetition_rating_target)
    rating += influence['equal_consecutive_notes_rating'] * abs(equal_consecutive_notes_rating - equal_consecutive_notes_rating_target)
    rating += influence['unique_rhythm_values'] * abs(unique_rhythm_values - unique_rhythm_values_target)
    total_influence = (influence['crazy_rating'] + influence['direction_of_melody'] +
                       influence['direction_stability'] + influence['pitch_range'] + influence['repetition_rating'] + 
                        influence['equal_consecutive_notes_rating'] + influence['unique_rhythm_values']
                       )
    final_rating = rating / total_influence

    # Create a dictionary of ratings
    song_ratings = {
        "Crazy Rating": crazy_rating,
        "Direction of Melody": direction_of_melody,
        "Direction Stability": direction_stability,
        "Pitch Range": pitch_range,
        "Repetition Rating": repetition_rating,
        "Equal Consecutive Notes Rating": equal_consecutive_notes_rating,
        "Unique Rhythm Values": unique_rhythm_values,
        "Final Rating": final_rating
    }
    return song_ratings

# List of files to rate
songs_to_rate = ['./midi_files/loser.mid', './midi_files/home_riff.mid', './midi_files/dead_memories.mid']

# Collect results
results = {}
for song in songs_to_rate:
    results[song] = rate_a_song(song)

# Display results in a table
df = pd.DataFrame.from_dict(results, orient='index')
df.index.name = 'Song Name'
print(df.to_string())
df.to_csv('song_ratings.csv')

# print('a loser is rated', rate_a_song('./midi_files/loser.mid'))
# print('Home_riff is rated', rate_a_song('./midi_files/home_riff.mid')) 
# print('pain_riff is rated', rate_a_song('./midi_files/dead_memories.mid')) 
# kryptonite is rated 0.047305177077739013
# duckandrun is rated 0.03840373113228471
# whenimgone is rated 0.028058219781743193
print('test.mid is rated', rate_a_song('./test.mid'))