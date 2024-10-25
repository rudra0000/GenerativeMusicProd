import mido
import random
import matplotlib.pyplot as plt
POPULATION_SIZE=10
MUTATE_FRACTION=0.2
# Load the original MIDI file (for example, 'finalcountdown.mid')
cv1 = mido.MidiFile('alan_walker_-_alone.mid', clip=True)

# Select the track you want to isolate (for example, track 0)
source_track = cv1.tracks[1]
# print('source trtack len', len(source_track))
# print('source trtac',(source_track))

# Create a new MIDI file and a new track
new_mid = mido.MidiFile()
new_track = mido.MidiTrack()
# print(source_track)
# Optional: Add some meta messages for tempo, key signature, etc.
# new_track.append(mido.MetaMessage('key_signature', key='C'))
# new_track.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(40)))
# new_track.append(mido.MetaMessage('time_signature', numerator=6, denominator=8))

# Copy the events from the source track to the new track
# abc = 5


filterthese = ['track_name', 'end_of_track', 'key_signature', 'set_tempo', 'time_signature']
for msg in source_track:
    # We only append musical or relevant events, skipping others like SysEx, etc.
    # msg.is_meta or type(msg) is mido.messages.messages.Message or 
    if msg.type in filterthese:
        print('incoming kombucha - ', msg)
        # above this we see the req meta messgaeese
    else:
        if msg.type == 'note_on' or msg.type == 'note_off':
            msg = mido.Message('note_on', channel=7, note=msg.note, velocity=msg.velocity, time=msg.time)
            new_track.append(msg)
        pass

# new_track.append(mido.MetaMessage('end_of_track'))


# new track does not have any 

# Append the new track to the new MIDI file
new_mid.tracks.append(new_track)
print('new track 5f 5l')
print(new_track[:5], new_track[-5:])



# Save the new MIDI file with the isolated track and added notes
new_mid.save('isolated_track_with_notes.mid')

print("Isolated track with added notes saved to 'isolated_track_with_notes.mid'")
# print(new_track)


#takes a track and returns list of inidviduals(tracks)
def generatePopulation(track):
    population = [track.copy() for _ in range(POPULATION_SIZE)]
    for individual in population:
        evolve(individual)

    return population

def evolve(individual):
    size=len(individual)
    assert(size%2==0)
    start=2*random.randint(1,size//2)-1
    end=start+int(size*MUTATE_FRACTION)

    if end>=size:
        end=size-1
    print(len(mutate(individual=individual,start_index=start,end_index=end)))
    print(end-start+1)
    individual[start:end+1]=mutate(individual=individual,start_index=start,end_index=end)
    

#chromosome:subpart of a track
#takes a chromosome and randomly mutate note(s) (returns)
def mutate(individual,start_index,end_index):
    old_l =  individual[start_index:end_index+1]
    l = individual[start_index:end_index+1]
    random.shuffle(l)
    flag = all(x == y for x, y in zip(old_l, l))
    assert(not flag)
    return l



#takes two individuals
#crossover about a point
def crossover():
    pass

population=generatePopulation(new_track)
print(len(population[0]))


x_list = [i for i in range(0,len(population[0]))]
y_list=[msg.note for msg in population[0]]
plt.scatter(x_list, y_list, label="track1",color='blue')

x_list2 = [i for i in range(0,len(population[1]))]
y_list2=[msg.note for msg in population[1]]
plt.scatter(x_list, y_list2, label="track2",color='red')

plt.show()
plt.close()