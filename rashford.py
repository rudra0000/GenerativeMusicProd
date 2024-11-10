import mido
FILENAME='./duckandrun.mid'
midi_data=mido.MidiFile(filename=f'./midi_files/{FILENAME}')

# class CustomMetaMessage(mido.MetaMessage):
#     def __init__(self, type, skip_checks=False, **kwargs):
#         super().__init__(type, skip_checks=False, **kwargs)

#         self.actual_time = 0
midi_track0 = midi_data.tracks[0]

def fwrite(str1, filename):
    with open(filename, 'a') as f:
        f.write(str1 + "\n")


def pretty_print_arr(arr):
    print("[")
    for i in arr:
        print(i)
    print("]")

f = open("intermediate.txt","w")
def print_object_attributes(objects):
    for obj in objects:
        # Get the attributes of the object as a dictionary
        attributes = vars(obj)
        # Print each attribute's name and value in a single line
        # print(" | ".join(f"{key}={value}" for key, value in attributes.items()))
        
        f.write(" | ".join(f"{key}={value}" for key, value in attributes.items()))
        f.write("\n")


class CustomMetaMessage:
    def __init__(self, type, skip_checks=False, **kwargs):
        # Initialize the MetaMessage
        self.meta_message = mido.MetaMessage(type, skip_checks=skip_checks, **kwargs)
        # Store the actual time separately
        self.actual_time = 0

    def __getattr__(self, name):
        # Forward any attribute lookup to the underlying MetaMessage object
        return getattr(self.meta_message, name)

    def __setattr__(self, name, value):
        if name != "meta_message" and name != "actual_time":
            # Forward setting other attributes to the underlying MetaMessage object
            setattr(self.meta_message, name, value)
        else:
            super().__setattr__(name, value)

    def __str__(self):
        return f'MetaMessage type: {self.type}, time: {self.time}, actual_time: {self.actual_time}'



class CustomMessage:
    def __init__(self, type, skip_checks=False, extra_info=None, **args):
        # Initialize the base Message object
        self.message = mido.messages.messages.Message(type, **args)
        # self.message = mido.Message(type, **args)
        # Store the actual time separately
        self.actual_time = 0

    def __getattr__(self, name):
        # Forward any attribute lookup to the underlying mido.Message object
        return getattr(self.message, name)

    def __setattr__(self, name, value):
        if name not in ['message', 'actual_time']:
            # Forward setting other attributes to the underlying mido.Message object
            setattr(self.message, name, value)
        else:
            super().__setattr__(name, value)
    def __str__(self):
        if self.type == 'note_on':
            return f'Message(notes) type: {self.type}, time: {self.time}, actual_time: {self.actual_time}, note: {self.note}, velocity: {self.velocity}'
        else:
            return f'type: {self.type}, time: {self.time}, actual_time: {self.actual_time}'

class Note_rep:
    def __init__(self):
        self.type = ''
        self.channel=0
        self.note = ''
        self.velocity=0
        self.start_time=0
        self.duration=0
        self.time = 0
    
    def __init__(self, channel=0, note='', velocity=0, start_time=0, duration=0,time=0):
        self.channel=channel
        self.note = note
        self.velocity=velocity
        self.start_time=start_time
        self.duration=duration
        self.time = time
    
    def __init__(self, obj, duration=0): # use this
        self.type = 'note'
        
        self.obj = obj
       
        if obj.type == 'note_on':
            self.channel = obj.channel
            self.note = obj.note
            self.velocity = obj.velocity
            self.start_time = obj.actual_time
            self.duration = duration
            self.time = obj.time
        else:
            self.time = obj.time
            self.type = 'not_note'

    # def __init__(self, obj, duration=0): # we use the last two constructors
    #     self.type = 'not_note'
    #     self.channel = obj.channel
    #     self.note = obj.note
    #     self.velocity = obj.velocity
    #     self.start_time = obj.actual_time
    #     self.duration = duration

    def __str__(self):
        if self.type == 'note':
            return f'type:{self.type} channel: {self.channel}, note: {self.note}, velocity: {self.velocity}, start_time: {self.start_time}, duration: {self.duration}'      
        else:
            return f'type: {self.type}, obj: {self.obj}'

#output intermediate
def conv_from_midi(track):
    intermediate = []
    curr_time = 0
    desirable = []
    for msg in track:
        curr_time += msg.time
        if msg.is_meta:
            custom_meta = CustomMetaMessage(type=msg.type)
            custom_meta.meta_message = msg
            custom_meta.actual_time = curr_time
            intermediate.append(custom_meta)
        elif msg.type in ['note_on', 'note_off']:
            custom_message = CustomMessage(msg.type)
            
            # Copy attributes from msg to custom_message
            custom_message.time = msg.time
            custom_message.actual_time = curr_time
            custom_message.velocity = msg.velocity  # Ensure velocity is copied correctly
            custom_message.note = msg.note          # Copy note if needed

            intermediate.append(custom_message)
        else:
            print(msg.type)
            intermediate.append(msg)
    print("-------")
    print(len(intermediate))
    print(len(track))
    # intermediate done
    for i in range(len(intermediate)):
        custom_msg=intermediate[i]
        
        if custom_msg.type=='note_on' and custom_msg.velocity != 0:
            # print(intermediate[i].type)
            for j in range(i+1,len(intermediate)):
                higher_lvl_message = intermediate[j]
                condition1 = (isinstance(intermediate[j], CustomMessage)) and (higher_lvl_message.type == 'note_off') and (higher_lvl_message.note == custom_msg.note)
                condition2 = (higher_lvl_message.type == 'note_on') and (higher_lvl_message.note == custom_msg.note) and (higher_lvl_message.velocity == 0)
                if condition1 or condition2 :
                    # assume that all note_on with vel=0 are converted to note_off events
                    duration = intermediate[j].actual_time - custom_msg.actual_time
                    note_rep = Note_rep(custom_msg, duration=duration)
                    desirable.append(note_rep)
                    break
        elif custom_msg.type == 'note_off':
            pass
        else :
            note_rep = Note_rep(custom_msg, duration=0)
            desirable.append(note_rep)
            # print('NOTA')
            pass
            # print(intermediate[j].velocity)
            # print(intermediate[j].type)

    for line in intermediate:
        fwrite(line.__str__(), 'intermediate.txt')
    for line in desirable:
        fwrite(line.__str__(), 'desirable.txt')

    return desirable

def save_track_to_midi(track2, output_file_path):
    # Create a new MIDI file and a track
    global midi_track0
    midi = mido.MidiFile()
    midi_track = mido.MidiTrack()
    midi.tracks.append(midi_track0)
    midi.tracks.append(midi_track)
    print("-------")
    print(len(track2))
    # Add messages to the track
    for msg in track2:
        if isinstance(msg, mido.MetaMessage):
            midi_track.append(msg)  # Add meta messages directly
        elif isinstance(msg, mido.messages.messages.Message):
            midi_track.append(msg)  # Add regular messages directly
        else:
            print(f"Skipping unknown message type: {msg}")

    # Save the MIDI file
    midi.save(output_file_path)
    print(f"MIDI file saved to {output_file_path}")

def conv_to_midi(converted):
    intermediate2 = []
    for note_rep in converted:
        if note_rep.type == 'note':
            note_on = CustomMessage('note_on', channel=note_rep.channel, note=note_rep.note, velocity=note_rep.velocity,time=note_rep.time)
            note_off = CustomMessage('note_off', channel=note_rep.channel, note=note_rep.note, velocity=0,time=note_rep.time)
            intermediate2.append(note_on)
            intermediate2.append(note_off)
        else:
            intermediate2.append(note_rep.obj)
    for line in intermediate2:
        fwrite(line.__str__(), 'intermediate2.txt')
    track2 = []
    for msg in intermediate2:
        if isinstance(msg, CustomMetaMessage):
            track2.append(msg.meta_message)
        elif isinstance(msg, CustomMessage):
            track2.append(msg.message)
        else:
            track2.append(msg)
    # put this track2 in a midi file    
    return track2

converted=conv_from_midi(midi_data.tracks[2])
track2 = conv_to_midi(converted)

track = midi_data.tracks[1]
with open ('track', 'w') as file:
    for element in track:
        file.write(str(element) + '\n')

with open ('track2', 'w') as file:
    for element in track2:
        file.write(str(element) + '\n')
save_track_to_midi(track, 'output.mid')
save_track_to_midi(track, 'input.mid')
for i in range(0, len(track2)):
    if (track2[i] != track[i]):
        print(i)
        print(track2[i])
        print(track[i])
        break

# print(midi_data.tracks[0]['set_tempo'])
f.close()