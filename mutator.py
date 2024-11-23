
import random
import rashford
import math
def pitch_mutator(track,range1,prob_mutation=0.3,prob_distribution=None):
    for i in range(len(track)):
        if (track[i].type != 'note'):
            continue
        old_note = track[i].note
        lower_limit = max(0,old_note-range1)
        upper_limit = min(127,old_note+range1)
        options = list(range(lower_limit,upper_limit+1))
        if random.random() < prob_mutation:
            track[i].note = random.choice(options)
    return track
    pass
def start_time_mutator(track,range1,prob_mutation=0.3,prob_distribution=None):
    hcf = 0
    for i in range(len(track)):
        if (track[i].type != 'note'):
            continue
        hcf = math.gcd(hcf,track[i].start_time)
    
    for i in range(len(track)):
        if (track[i].type != 'note'):
            continue
        old_start_time = track[i].start_time
        lower_limit = max(0,old_start_time-range1)
        upper_limit = min(127,old_start_time+range1)
        options = list(range(0,hcf*3+1,hcf))
        if random.random() < prob_mutation:
            track[i].start_time = random.choice(options)
    return track
    pass