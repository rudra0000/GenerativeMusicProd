import random
import mido
import format_conversion


precision=1000
track1_time = 0
track2_time = 0

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



