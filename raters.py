import os
def neighboring_pitch_range(track,range1):
    # No of Crazy Notes
    # detect notes with pitch value atleast one octave away from the previous note
    # return the number of such notes
    crazy_notes = 0
    total_notes = 0
    prev_note = -1
    for i in range(len(track)):
        if (track[i].type != 'note'):
            continue
        total_notes += 1
        if (i == 0):
            continue
        if ((prev_note != -1) and abs(track[i].note - prev_note) > range1):
            crazy_notes += 1
        prev_note = track[i].note
    return crazy_notes/total_notes

def direction_of_melody(track,range1):
    # No of pitches higher than the previous note divided by the total number of notes
    # return the ratio
    higher_notes = 0
    total_notes = 0
    prev_note = -1
    for i in range(len(track)):
        if (track[i].type != 'note'):
            continue
        total_notes += 1
        if (i == 0):
            continue
        if (track[i].note > prev_note):
            higher_notes += 1
        prev_note = track[i].note
    return higher_notes/total_notes

def direction_stability(track):
#     The purpose of this sub-rater is to determine the amount of changes in pitch direction
#  within a track. The sub-rater iterates through every note in a track, counts the number
#  of times the pitch value changes direction, and calculates the rating using equation below:
#  R = Number of pitch direction changes / Total number of notes
    pitch_changes = 0
    total_notes = 0
    prev_note = -1
    prev_direction = 0
    for i in range(len(track)):
        if (track[i].type != 'note'):
            continue
        total_notes += 1
        if (i == 0):
            continue
        if (prev_note == -1):
            prev_note = track[i].note
            continue
        if (prev_note < track[i].note):
            direction = 1
        else:
            direction = -1
        if (prev_direction != direction):
            pitch_changes += 1
        prev_direction = direction
        prev_note = track[i].note
    return pitch_changes/total_notes

def pitch_range(track):
#      The purpose this sub-rater is to determine the pitch range between the highest and lowest
#  pitch values in a track. The sub-rater iterates through every note in a track, nds the
#  highest and lowest pitch, and calculates the rating using equation 13 below:
#  R= Lowest pitch value/Highest pitch value
    lowest_pitch = 127
    highest_pitch = 0
    for i in range(len(track)):
        if (track[i].type != 'note'):
            continue
        if (track[i].note < lowest_pitch):
            lowest_pitch = track[i].note
        if (track[i].note > highest_pitch):
            highest_pitch = track[i].note
    return lowest_pitch/highest_pitch

def unique_note_pitches(track):
#      The purpose of this sub-rater is to determine how many unique note pitches that are
#  being used in the music segment. It rarley occurs that music contains only one or two dif
# ferent note pitches, a decent variety of them is necessary to assure quality. The sub-rater
#  iterates through every note in a track, nds all unique notes, and calculates the rating
#  using equation 16 below:
#  R= Number of unique note pitches
#  Total number of notes
    unique_notes = set()
    total_notes = 0
    for i in range(len(track)):
        if (track[i].type != 'note'):
            continue
        total_notes += 1
        unique_notes.add(track[i].note)
    return len(unique_notes)/total_notes

def equal_consecutive_notes(track):
#     The purpose of this sub-rater is to rate how many times two consecutive notes share the
#  same pitch value. The sub-rater iterates through every note in a track, nds all note pairs
#  who share the same pitch value, and calculates the rating using equation 17 below:
#  R= Number of two consecutive notes with the same pitch
#  Total number of notes
    consecutive_notes = 0
    total_notes = 0
    prev_note = -1
    for i in range(len(track)):
        if (track[i].type != 'note'):
            continue
        total_notes += 1
        if (i == 0):
            continue
        if (prev_note == track[i].note):
            consecutive_notes += 1
        prev_note = track[i].note
    return consecutive_notes/total_notes

def unique_rythm_values(track):
#     The purpose of this sub-rater is to rate the variety of rhythm values, which can be de ned
#  as the duration of the notes. The necessity of this rater is based on the fact that di erent
#  genres di er greatly in rhythm diversity. Simple melodies tend to keep the same rhythm
#  while more complex music can di er greatly throughout a song.
#  The sub-rater iterates through every note in a track, nds each unique rhythmvalue,
#  and calculates the rating using equation 18 below:
#  R= Unique rhythm values
#  Total number of notes
    unique_rhythms = set()
    total_notes = 0
    for i in range(len(track)):
        if (track[i].type != 'note'):
            continue
        total_notes += 1
        unique_rhythms.add(track[i].duration)
    return len(unique_rhythms)/total_notes
    pass

from collections import defaultdict

def build_suffix_array(sequence):
    """
    Constructs a suffix array for the given sequence and its LCP array.
    """
    n = len(sequence)
    suffixes = sorted((sequence[i:], i) for i in range(n))
    suffix_array = [suffix[1] for suffix in suffixes]
    lcp = [0] * n

    rank = [0] * n
    for i, suffix_index in enumerate(suffix_array):
        rank[suffix_index] = i

    k = 0
    for i in range(n):
        if rank[i] == n - 1:
            k = 0
            continue
        j = suffix_array[rank[i] + 1]
        while i + k < n and j + k < n and sequence[i + k] == sequence[j + k]:
            k += 1
        lcp[rank[i]] = k
        if k > 0:
            k -= 1

    return suffix_array, lcp


def find_repeated_patterns(sequence, min_length):
    """
    Finds all repeated patterns in the sequence with a minimum length.
    """
    suffix_array, lcp = build_suffix_array(sequence)
    patterns = defaultdict(list)

    for i in range(1, len(lcp)):
        if lcp[i] >= min_length:
            pattern = sequence[suffix_array[i]:suffix_array[i] + lcp[i]]
            patterns[tuple(pattern)].append(suffix_array[i])

    return patterns


def repetition_rating(track):
    """
    Calculates the repetition rating of a track.
    
    Parameters:
    - track: A list of pitches or rhythm values.
    
    Returns:
    - Repetition rating (float).
    """
    if not track:
        return 0.0

    min_length = max(1, int(len(track) * 0.01))  # 1% of total track length
    patterns = find_repeated_patterns(track, min_length)

    # Calculate the number of values covered by patterns
    covered = set()
    for pattern, positions in patterns.items():
        for pos in positions:
            for i in range(len(pattern)):
                covered.add(pos + i)

    return len(covered) / len(track)

def calculate_scale_pattern_rating(track_notes):
    """
    Calculate the scale pattern rating for a given track.

    Parameters:
    - track_notes (list): List of notes (integers or floats representing pitches in the track).
    - scale_notes (list): List of notes in the scale (e.g., a diatonic scale).

    Returns:
    - float: The scale pattern rating R(r).
    """
    scale_notes = [0, 2, 4, 5, 7, 9, 11]
    N = len(scale_notes)  # Number of notes in the scale pattern
    total_notes = len(track_notes)  # Total number of notes in the track

    if total_notes == 0:
        raise ValueError("The track has no notes to analyze.")

    # Count how many notes in the track fit the scale pattern
    notes_in_scale = sum(1 for note in track_notes if (note.type == 'note') and note.note % 12 in scale_notes)

    # Calculate the raw rating 'r'
    r = notes_in_scale / total_notes

    # Calculate the final normalized rating R(r)
    R_r = (12 * r - N) / (12 - N)

    return max(0, min(R_r, 1))  # Ensure the result is clamped between 0 and 1


def equal_consecutive_notes(track):
    """
    Rates how many times two consecutive notes share the same pitch value.
    
    Args:
    track (list): A list of note objects, each having a 'pitch' attribute.
    
    Returns:
    float: The rating calculated as the number of consecutive notes with the same pitch
           divided by the total number of notes.
    """
    if not track:
        return 0.0
    
    consecutive_same_pitch = 0
    total_notes = 0
    previous_note = None
    
    for item in track:
        if hasattr(item, 'note'):
            total_notes += 1
            if previous_note is not None and item.note == previous_note.note:
                consecutive_same_pitch += 1
            previous_note = item
    
    if total_notes == 0:
        return 0.0
    
    return consecutive_same_pitch / total_notes

def unique_rhythm_values(track):
    """
    Rates the variety of rhythm values in a track.
    
    Args:
    track (list): A list of note objects, each having a 'duration' attribute.
    
    Returns:
    float: The rating calculated as the number of unique rhythm values divided by the total number of notes.
    """
    if not track:
        return 0.0
    
    unique_rhythms = set(note.duration for note in track)
    total_notes = len(track)
    
    return len(unique_rhythms) / total_notes


def repetition_rating(track):
    """
    Identifies repetitions in the track and calculates the repetition rating.
    
    Args:
    track (list): A list of note objects, each having 'pitch' and 'duration' attributes.
    
    Returns:
    float: The rating calculated as the number of pitch or rhythm values within patterns
           divided by the total number of pitch or rhythm values.
    """
    if not track:
        return 0.0
    
    # Convert track to a string of pitches for pattern detection
    pitch_sequence = ''.join(str(note.note) for note in track if note.type == 'note')
    
    # Find all repeating patterns using a suffix array approach
    suffixes = sorted((pitch_sequence[i:], i) for i in range(len(pitch_sequence)))
    lcp = [0] * len(suffixes)
    
    for i in range(1, len(suffixes)):
        lcp[i] = len(os.path.commonprefix([suffixes[i - 1][0], suffixes[i][0]]))
    
    # Identify patterns that are at least 1% of the total track length
    min_pattern_length = max(1, len(track) // 100)
    patterns = [suffixes[i][0][:lcp[i]] for i in range(1, len(lcp)) if lcp[i] >= min_pattern_length]
    
    # Sort patterns by how much of the track they cover
    patterns = sorted(set(patterns), key=lambda p: -pitch_sequence.count(p) * len(p))
    
    # Calculate the rating
    covered_values = sum(pitch_sequence.count(p) * len(p) for p in patterns)
    total_values = len(pitch_sequence)
    
    return covered_values / total_values