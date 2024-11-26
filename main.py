import rashford
import mido
import mutator
import raters

# FILENAME='./midi_files/duckandrun.mid'
# FILENAME='./midi_files/whenimgone.mid'
FILENAME='./midi_files/kryptonite.mid'
midi_data=mido.MidiFile(filename=f'{FILENAME}')

midi_track0 = midi_data.tracks[0]



# midi_track1 = midi_data.tracks[1]
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
    mutated_track = mutator.actual_time_mutator(desired_track, 5, 0.1)
    mutated_track = mutator.pitch_mutator(mutated_track, 5, 0.1)
    mutated_track = mutator.simplify_mutator(mutated_track, 5, 0.3)
    # print(f'CrazyRating: {raters.neighboring_pitch_range(desired_track, 12)}')
    # print(f'DirectionOfMelody: {raters.direction_of_melody(desired_track, 12)}')
    # print(f'DirectionStability: {raters.direction_stability(desired_track)}')
    # print(f'PitchRange : {raters.pitch_range(desired_track)}')
    # print(f'scaleRating: {raters.calculate_scale_pattern_rating(desired_track)}')
    for line in mutated_track:
        rashford.fwrite(line.__str__(), './debug_files/mutated_track.txt')
    midi_track1 = rashford.conv_to_midi(mutated_track)
    new_song.append(midi_track1)
  
print("###################################################################")
for i in midi_data.tracks:
    midi_track1 = i
    if (midi_track1 == midi_track0):
        continue
    desired_track =  rashford.conv_from_midi(midi_track1)
    # print(f'CrazyRating: {raters.neighboring_pitch_range(desired_track, 12)}')
    # print(f'DirectionOfMelody: {raters.direction_of_melody(desired_track, 12)}')
    # print(f'DirectionStability: {raters.direction_stability(desired_track)}')
    # print(f'PitchRange : {raters.pitch_range(desired_track)}')
    # print(f'scaleRating: {raters.calculate_scale_pattern_rating(desired_track)}')

rashford.save_track_to_midi(new_song, './test.mid',init_track=midi_track0)

# any song's crazy rating is the song's first track's crazy rating

rating_dict = {} # maps the song's name to its a dictionary of its ratings

best_files =['./midi_files/loser.mid', './midi_files/kryptonite.mid', './midi_files/duckandrun.mid', './midi_files/whenimgone.mid']
crazy_ratings_sum = 0
direction_of_melody_sum = 0
direction_stability_sum = 0
pitch_range_sum = 0
scale_rating_sum = 0

scale_rating_target = 0
pitch_range_target = 0
direction_stability_target = 0
direction_of_melody_target = 0
crazy_rating_target = 0
scale_rating_max = 0
pitch_range_max = 0
direction_stability_max = 0
direction_of_melody_max = 0
crazy_rating_max = 0
scale_rating_min = 0
pitch_range_min = 0
direction_stability_min = 0
direction_of_melody_min = 0
crazy_rating_min = 0

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
    pitch_range_sum += rating_dict[file]['pitch_range']
    rating_dict[file]['scale_rating'] = raters.calculate_scale_pattern_rating(midi_track1)
    scale_rating_sum += rating_dict[file]['scale_rating']
    scale_rating_max = max(scale_rating_max, rating_dict[file]['scale_rating'])
    pitch_range_max = max(pitch_range_max, rating_dict[file]['pitch_range'])
    direction_stability_max = max(direction_stability_max, rating_dict[file]['direction_stability'])
    direction_of_melody_max = max(direction_of_melody_max, rating_dict[file]['direction_of_melody'])
    crazy_rating_max = max(crazy_rating_max, rating_dict[file]['crazy_rating'])
    scale_rating_min = min(scale_rating_min, rating_dict[file]['scale_rating'])
    pitch_range_min = min(pitch_range_min, rating_dict[file]['pitch_range'])
    direction_stability_min = min(direction_stability_min, rating_dict[file]['direction_stability'])
    direction_of_melody_min = min(direction_of_melody_min, rating_dict[file]['direction_of_melody'])
    crazy_rating_min = min(crazy_rating_min, rating_dict[file]['crazy_rating'])


scale_rating_target = scale_rating_sum/len(best_files)
pitch_range_target = pitch_range_sum/len(best_files)
direction_stability_target = direction_stability_sum/len(best_files)
direction_of_melody_target = direction_of_melody_sum/len(best_files)
crazy_rating_target = crazy_ratings_sum/len(best_files)

influence = {}
influence['scale_rating'] = 2*abs(0.5 - min(scale_rating_target - scale_rating_min,scale_rating_max - scale_rating_target))
influence['pitch_range'] = 2*abs(0.5 - min(pitch_range_target - pitch_range_min,pitch_range_max - pitch_range_target))
influence['direction_stability'] = 2*abs(0.5 - min(direction_stability_target - direction_stability_min,direction_stability_max -direction_stability_target))
influence['direction_of_melody'] = 2*abs(0.5 - min(direction_of_melody_target - direction_of_melody_min,direction_of_melody_max - direction_of_melody_target))
influence['crazy_rating'] = 2*abs(0.5 - min(crazy_rating_target - crazy_rating_min,crazy_rating_max - crazy_rating_target))

def rate_a_song(file):
    midi_data=mido.MidiFile(filename=f'{file}')
    midi_track0 = midi_data.tracks[0]
    midi_track1 = midi_data.tracks[1]
    midi_track1 = rashford.conv_from_midi(midi_track1)
    rating = 0
    rating += influence['crazy_rating'] * abs(raters.neighboring_pitch_range(midi_track1, 12) - crazy_rating_target)
    rating += influence['direction_of_melody'] * abs(raters.direction_of_melody(midi_track1, 12) - direction_of_melody_target)
    rating += influence['direction_stability'] * abs(raters.direction_stability(midi_track1) - direction_stability_target)
    rating += influence['pitch_range'] * abs(raters.pitch_range(midi_track1) - pitch_range_target)
    rating += influence['scale_rating'] * abs(raters.calculate_scale_pattern_rating(midi_track1) - scale_rating_target)
    total_influence = influence['crazy_rating'] + influence['direction_of_melody'] + influence['direction_stability'] + influence['pitch_range'] + influence['scale_rating']
    rating = rating/total_influence
    return rating

# print('a loser is rated', rate_a_song('./midi_files/loser.mid')) #-0.03959
print('kryptonite is rated', rate_a_song('./midi_files/kryptonite.mid')) 
print('duckandrun is rated', rate_a_song('./midi_files/duckandrun.mid'))
print('whenimgone is rated', rate_a_song('./midi_files/whenimgone.mid')) 
print('test.mid is rated', rate_a_song('./test.mid'))