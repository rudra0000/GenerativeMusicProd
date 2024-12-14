import mido
import random,math
import matplotlib.pyplot as plt
POPULATION_SIZE=10
MUTATE_FRACTION=0.3
MUTATION_ITERATIONS=2000
# Load the original MIDI file (for example, 'finalcountdown.mid')
cv1 = mido.MidiFile('FOB_swgd.mid', clip=True)
# cv1 = mido.MidiFile('finalcountdown.mid', clip=True)

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
meta_messages=[]
for msg in source_track:
    # We only append musical or relevant events, skipping others like SysEx, etc.
    # msg.is_meta or type(msg) is mido.messages.messages.Message or 
    # if msg.type in filterthese:
    #     print('incoming kombucha - ', msg)
    #     # above this we see the req meta messgaeese
    # else:
    #     if msg.type == 'note_on' or msg.type == 'note_off':
    #         msg = mido.Message('note_on', channel=7, note=msg.note, velocity=msg.velocity, time=msg.time)
    #         new_track.append(msg)
    #     pass
        if msg.type == 'note_on' or msg.type == 'note_off':
            msg = mido.Message('note_on', channel=7, note=msg.note, velocity=msg.velocity, time=msg.time)
            new_track.append(msg)
        else:
            # print(msg.type)
            if msg.type not in ['program_change','pitchwheel','control_change']:
                meta_messages.append(msg)
            

# print(meta_messages)

# new_track.append(mido.MetaMessage('end_of_track'))


# new track does not have any 

# Append the new track to the new MIDI file

new_mid.tracks.append(new_track)
# print('new track 5f 5l')
# print(new_track[:5], new_track[-5:])



# Save the new MIDI file with the isolated track and added notes
new_mid.save('isolated_track_with_notes.mid')

# print("Isolated track with added notes saved to 'isolated_track_with_notes.mid'")
# print(new_track)


#takes a track and returns list of inidviduals(tracks)
def generatePopulation(track):
    population = [track.copy() for _ in range(POPULATION_SIZE)]
        
    for i in range(len(population)):
        individual=population[i]
        for j in range(MUTATION_ITERATIONS):
            evolve(individual)
        meta_messages.append(mido.MetaMessage('key_signature', key='C'))
        meta_messages.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(180)))
        meta_messages.append(mido.MetaMessage('time_signature', numerator=6, denominator=8))
        for msg in meta_messages:
            if msg.type=='end_of_track':
                individual.append(msg)
            else:
                individual[:0]=[msg]
        new_mid = mido.MidiFile()
        # new_track = mido.MidiTrack()
        new_mid.tracks.append(individual)
        new_mid.save(f'isolated_track_with_notes{i}.mid')
    
    return population
    
# def generateWorld(track):
#     for i in range(MUTATION_ITERATIONS):
#         population=generatePopulation(track)
#         track=population[1][:]
#     return population

def evolve(individual):
    size=len(individual)
    # assert(size%2==0)
    # print(size)
    if size < 2:
        print('Individual is too small')
        return
    start=2*(random.randint(1,size//2)-1)
    end=start+math.ceil(size*MUTATE_FRACTION)

    if end>=size:
        end=size-1

    if end%2 == 0:
        end-=1

    
    assert((end-start+1)%2==0)
    # print(len(mutate(individual=individual,start_index=start,end_index=end)))
    # print(end-start+1)
    b4 = len(individual)
    temp_list = mutate(individual=individual,start_index=start,end_index=end)
    individual[start:end+1]=temp_list
    if b4-len(individual) != 0:
        print('the difference is', b4-len(individual))
        print('rhs lenght returned', len(temp_list))
        print('lhs lenght is', len(individual[start:end+1]))
        # this means that the mutate length returned is lesser
    assert(b4-len(individual) == 0)
    

#chromosome:subpart of a track
#takes a chromosome and randomly mutate note(s) (returns)
def mutate(individual,start_index,end_index):
    old_l =  individual[start_index:end_index+1]
    l = []
    indexes=[i for i in range(0,(end_index-start_index+1)//2)] ##########################
    random.shuffle(indexes)

    
    for index in indexes:
        l.append(old_l[2*index])
        l.append(old_l[2*index+1])

    # print('l is ', len(l))
    # print('individual lengthhh is ', len(individual))
    flag = all(x == y for x, y in zip(old_l, l))
    # assert(not flag)
    return l



#takes two individuals
#crossover about a point
def crossover():
    pass

# population=generateWorld(new_track)
population=generatePopulation(new_track)
# print(len(population[0]))


# x_list = [i for i in range(0,len(population[0]))]
# y_list=[msg.note for msg in population[0]]
# plt.scatter(x_list, y_list, label="track1",color='blue')

# x_list2 = [i for i in range(0,len(population[1]))]
# y_list2=[msg.note for msg in population[1]]
# plt.scatter(x_list, y_list2, label="track2",color='red')

# plt.show()
# plt.close(
