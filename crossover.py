import random
import mido
import rashford


precision=1000
track1_time = 0
track2_time = 0
def crossover(track1,track2): # return both the tracks after crossover
    #normalize the tracks
    global track1_time
    global track2_time
    try:
        track1_time=track1[-2].actual_time+track1[-2].duration
        track2_time=track2[-2].actual_time+track2[-2].duration
    except:
        track1_time=track1[-2].actual_time+track1[-2].duration
        track2_time=track2[-2].actual_time+track2[-2].duration
    for i in range(len(track1)):
        try:
            track1[i].actual_time=int(track1[i].actual_time*track2_time)
            track1[i].duration=int(track1[i].duration*track2_time )
        except:
            track1[i].actual_time=int(track1[i].actual_time*track2_time )
            track1[i].duration=int(track1[i].duration*track2_time )
    for i in range(len(track2)):
        try:
            track2[i].actual_time=int(track2[i].actual_time*track1_time )
            track2[i].duration=int(track2[i].duration*track1_time )
        except:
            track2[i].actual_time=int(track2[i].actual_time*track1_time )
            track2[i].duration=int(track2[i].duration*track1_time)

    #crossover
    pt1,pt2=random.random()*track1_time*track2_time,random.random() * track1_time * track2_time
    pt1 = int(pt1)
    pt2 = int(pt2)
    if pt1>pt2:
        pt1,pt2=pt2,pt1
    new_track1=[]
    new_track2=[]
    track1_start,track1_end=-2,-2
    track2_start,track2_end=-2,-2
    
    for i in range(len(track1)):
        elem=track1[i]
        if elem.actual_time>=pt1 and track1_start==-2:
            track1_start=i
        if elem.actual_time<=pt2:
            track1_end=i
    for i in range(len(track2)):
        elem=track2[i]
        if elem.actual_time>pt1 and track2_start==-2:
            track2_start=i
        if elem.actual_time<=pt2:
            track2_end=i
    
    assert track1_start <= track1_end
    print(f"chosen indices are {track1_start} {track1_end}")
    # if track1_start > track1_end:
    #     track1_end, track1_start = track1_start, track1_end
    new_track1+=track1[:track1_start]
    new_track1+=track2[track2_start:track2_end]
    new_track1+=track1[track1_end:]
    new_track2+=track2[:track2_start]   
    new_track2+=track1[track1_start:track1_end]
    new_track2+=track2[track2_end:]

    return new_track1,new_track2


FILENAME1='./midi_files/dead_memories.mid'
FILENAME2='./midi_files/pain_riff.mid'
midi_data1=mido.MidiFile(filename=f'{FILENAME1}')
midi_track10 = midi_data1.tracks[0]

midi_data2=mido.MidiFile(filename=f'{FILENAME2}')
midi_track20 = midi_data1.tracks[0]


# rashford.pretty_print_arr(rashford.conv_from_midi(midi_data1.tracks[1]))
# print(rashford.conv_from_midi(midi_data2.tracks[1]))
new1 = rashford.conv_from_midi(midi_data1.tracks[1])
new2  = rashford.conv_from_midi(midi_data2.tracks[1])
for j in range(5):
    new1, new2 = crossover(new1, new2)
    for i in range(len(new1)):
        new1[i].actual_time=int(new1[i].actual_time //track2_time)
        new1[i].duration=int(new1[i].duration //track2_time)
    for i in range(len(new2)):
        new2[i].actual_time=int(new2[i].actual_time //track1_time)
        new2[i].duration=int(new2[i].duration //track1_time)
    print(f"after iteration{j}, ")
    rashford.pretty_print_arr(new1)
    rashford.pretty_print_arr(new2)
# Undo the scaling



new1 = rashford.conv_to_midi(new1)
new2 = rashford.conv_to_midi(new2)


midi_file1 = mido.MidiFile()
empty_track0 = mido.MidiTrack()
# empty_track0.append(mido.MetaMessage('set_tempo', tempo=3000000))
midi_file1.tracks.append(empty_track0)
midi_file1.tracks.append(new1)

midi_file2 = mido.MidiFile()
empty_track0 = mido.MidiTrack()
# empty_track0.append(mido.MetaMessage('set_tempo', tempo=3000000))
midi_file2.tracks.append(empty_track0)
midi_file2.tracks.append(new2)

midi_file1.save('./debug_files/crossover1.mid')
midi_file2.save('./debug_files/crossover2.mid')

