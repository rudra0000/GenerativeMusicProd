import random
import mido
import rashford


precision=1000
track1_time = 0
track2_time = 0
# def crossover(track1,track2): # return both the tracks after crossover
#     #normalize the tracks
#     global track1_time
#     global track2_time
#     try:
#         track1_time=track1[-2].actual_time+track1[-2].duration
#         track2_time=track2[-2].actual_time+track2[-2].duration
#     except:
#         track1_time=track1[-2].actual_time+track1[-2].duration
#         track2_time=track2[-2].actual_time+track2[-2].duration
#     for i in range(len(track1)):
#         try:
#             track1[i].actual_time=int(track1[i].actual_time*track2_time)
#             track1[i].duration=int(track1[i].duration*track2_time )
#         except:
#             track1[i].actual_time=int(track1[i].actual_time*track2_time )
#             track1[i].duration=int(track1[i].duration*track2_time )
#     for i in range(len(track2)):
#         try:
#             track2[i].actual_time=int(track2[i].actual_time*track1_time )
#             track2[i].duration=int(track2[i].duration*track1_time )
#         except:
#             track2[i].actual_time=int(track2[i].actual_time*track1_time )
#             track2[i].duration=int(track2[i].duration*track1_time)

#     #crossover
#     pt1,pt2=random.random()*track1_time*track2_time,random.random() * track1_time * track2_time
#     pt1 = int(pt1)
#     pt2 = int(pt2)
#     if pt1>pt2:
#         pt1,pt2=pt2,pt1
#     new_track1=[]
#     new_track2=[]
#     track1_start,track1_end=-2,-2
#     track2_start,track2_end=-2,-2
    
#     for i in range(len(track1)):
#         elem=track1[i]
#         if elem.actual_time>=pt1 and track1_start==-2:
#             track1_start=i
#         if elem.actual_time<=pt2:
#             track1_end=i
#     for i in range(len(track2)):
#         elem=track2[i]
#         if elem.actual_time>pt1 and track2_start==-2:
#             track2_start=i
#         if elem.actual_time<=pt2:
#             track2_end=i
    
#     assert track1_start <= track1_end
#     print(f"chosen indices are {track1_start} {track1_end}")
#     # if track1_start > track1_end:
#     #     track1_end, track1_start = track1_start, track1_end
#     new_track1+=track1[:track1_start]
#     new_track1+=track2[track2_start:track2_end]
#     new_track1+=track1[track1_end:]
#     new_track2+=track2[:track2_start]   
#     new_track2+=track1[track1_start:track1_end]
#     new_track2+=track2[track2_end:]

#     return new_track1,new_track2


def crossover_tracks_random(track1, track2, swap_probability=0.5):
    """
    Perform a crossover between two tracks of Note_rep objects with a given swap probability.
    Randomly generates swap_start and swap_end based on actual_time ranges of both tracks.
    
    Args:
        track1: List of Note_rep objects for track 1.
        track2: List of Note_rep objects for track 2.
        swap_probability: The probability (0 to 1) of performing the swap.
        
    Returns:
        new_track1, new_track2: Two new tracks with the swapped regions.
    """
    def get_time_bounds(track):
        """Get the minimum and maximum actual_time for the track."""
        if not track:
            return 0, 0
        min_time = min(note.actual_time for note in track)
        max_time = max(note.actual_time + note.duration for note in track)
        return min_time, max_time

    def get_valid_region(track, start, end):
        """Get notes from the track that are within the valid region for swapping."""
        valid_notes = []
        for note in track:
            note_start = note.actual_time
            note_end = note.actual_time + note.duration
            # Ensure the note is fully contained within the region
            if note_start >= start and note_end <= end:
                valid_notes.append(note)
        return valid_notes
    
    # Get time bounds for both tracks
    min_time1, max_time1 = get_time_bounds(track1)
    min_time2, max_time2 = get_time_bounds(track2)
    
    # Determine global bounds
    global_min_time = max(min_time1, min_time2)
    global_max_time = min(max_time1, max_time2)
    
    if global_min_time >= global_max_time:
        # No valid overlap in time ranges
        return track1, track2
    
    
    # Randomly select swap_start and swap_end within the valid range
    swap_start = random.randint(global_min_time, global_max_time - 1)
    swap_end = random.randint(swap_start + 1, global_max_time)
    
    # Decide whether to perform the swap based on probability
    if random.random() > swap_probability:
        # Skip swapping and return the original tracks
        return track1, track2
    
    # Get valid swap regions
    valid_region1 = get_valid_region(track1, swap_start, swap_end)
    valid_region2 = get_valid_region(track2, swap_start, swap_end)
    
    # Ensure new tracks start as copies of the originals
    new_track1 = track1[:]
    new_track2 = track2[:]
    
    # Remove valid regions from original tracks
    new_track1 = [note for note in new_track1 if note not in valid_region1]
    new_track2 = [note for note in new_track2 if note not in valid_region2]
    
    # Insert swapped regions
    new_track1.extend(valid_region2)
    new_track2.extend(valid_region1)
    
    # Sort by `actual_time` to maintain the proper order
    new_track1.sort(key=lambda note: note.actual_time)
    new_track2.sort(key=lambda note: note.actual_time)
    
    return new_track1, new_track2


# Example usage:
# Assuming `track1` and `track2` are lists of Note_rep objects
# new_track1, new_track2 = crossover_tracks_random(track1, track2)


# def crossover(track1, track2):
#     """
#     Perform crossover without renormalizing the entire track's timing.
#     Each track maintains its original timing structure.
#     """
#     # Define crossover points
#     track1_total_time = track1[-1].actual_time + track1[-1].duration
#     track2_total_time = track2[-1].actual_time + track2[-1].duration

#     pt1 = random.randint(0, min(track1_total_time, track2_total_time))
#     pt2 = random.randint(0, min(track1_total_time, track2_total_time))
#     if pt1 > pt2:
#         pt1, pt2 = pt2, pt1

#     # Split tracks into segments
#     track1_pre, track1_crossover, track1_post = [], [], []
#     track2_pre, track2_crossover, track2_post = [], [], []

#     for note in track1:
#         if note.actual_time < pt1:
#             track1_pre.append(note)
#         elif pt1 <= note.actual_time <= pt2:
#             track1_crossover.append(note)
#         else:
#             track1_post.append(note)

#     for note in track2:
#         if note.actual_time < pt1:
#             track2_pre.append(note)
#         elif pt1 <= note.actual_time <= pt2:
#             track2_crossover.append(note)
#         else:
#             track2_post.append(note)

#     # Combine segments to form new tracks
#     new_track1 = track1_pre + track2_crossover + track1_post
#     new_track2 = track2_pre + track1_crossover + track2_post

#     # Adjust crossover sections' timing to align seamlessly
#     align_crossover(new_track1, track1_pre, track2_crossover, pt1, pt2)
#     align_crossover(new_track2, track2_pre, track1_crossover, pt1, pt2)

#     return new_track1, new_track2


# def align_crossover(new_track, pre_segment, crossover_segment, pt1, pt2):
#     """
#     Align the crossover section timing with the pre and post segments.
#     """
#     # Adjust start times of the crossover section
#     if crossover_segment:
#         start_offset = pre_segment[-1].actual_time + pre_segment[-1].duration if pre_segment else 0
#         time_shift = start_offset - crossover_segment[0].actual_time

#         for note in crossover_segment:
#             note.actual_time += time_shift

#     # Ensure all notes after pt2 align seamlessly
#     for i in range(len(new_track)):
#         if new_track[i].actual_time > pt2:
#             new_track[i].actual_time += time_shift



# FILENAME1='./midi_files/duckandrun.mid'
# FILENAME2='./midi_files/alone_fixed.mid'
# midi_data1=mido.MidiFile(filename=f'{FILENAME1}')
# midi_track10 = midi_data1.tracks[0]

# midi_data2=mido.MidiFile(filename=f'{FILENAME2}')
# midi_track20 = midi_data1.tracks[0]


# # rashford.pretty_print_arr(rashford.conv_from_midi(midi_data1.tracks[1]))
# # print(rashford.conv_from_midi(midi_data2.tracks[1]))
# new1 = rashford.conv_from_midi(midi_data1.tracks[1])
# new2  = rashford.conv_from_midi(midi_data2.tracks[1])
# for j in range(5):
#     new1, new2 = crossover(new1, new2)
#     for i in range(len(new1)):
#         new1[i].actual_time=int(new1[i].actual_time/track2_time)
#         new1[i].duration=int(new1[i].duration/track2_time)
#     for i in range(len(new2)):
#         new2[i].actual_time=int(new2[i].actual_time/track1_time)
#         new2[i].duration=int(new2[i].duration/track1_time)
#     print(f"after iteration{j}, ")
#     rashford.pretty_print_arr(new1)
#     rashford.pretty_print_arr(new2)

# tempo1 = 500000
# tempo2 = 500000
# for i in range(len(midi_data1.tracks[0])):
#     if midi_data1.tracks[0][i].type == 'set_tempo':
#         tempo1 = midi_data1.tracks[0][i].tempo
#         break
# for i in range(len(midi_data2.tracks[0])):
#     if midi_data2.tracks[0][i].type == 'set_tempo':
#         tempo2 = midi_data2.tracks[0][i].tempo
#         break

# for j in range(5):
#     # Perform crossover with the custom function
#     new1, new2 = crossover_tracks_random(new1, new2)
    
#     # Print the result after each iteration
#     print(f"After iteration {j}:")
#     rashford.pretty_print_arr(new1)
#     rashford.pretty_print_arr(new2)

# Undo the scaling



# new1 = rashford.conv_to_midi(new1)
# new2 = rashford.conv_to_midi(new2)

# midi_file1 = mido.MidiFile()
# empty_track0 = mido.MidiTrack()
# # empty_track0.append(mido.MetaMessage('set_tempo', tempo=3000000))
# midi_file1.tracks.append(midi_data1.tracks[0])
# midi_file1.tracks.append(new1)

# midi_file2 = mido.MidiFile()
# # empty_track0.append(mido.MetaMessage('set_tempo', tempo=3000000))
# midi_file2.tracks.append(midi_data2.tracks[0])
# midi_file2.tracks.append(new2)

# midi_file1.save('./debug_files/crossover1.mid')
# midi_file2.save('./debug_files/crossover2.mid')


