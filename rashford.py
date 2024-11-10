import mido
FILENAME='alan_walker_-_alone.mid'
midi_data=mido.MidiFile(filename=f'./midi_files/{FILENAME}')

# class CustomMetaMessage(mido.MetaMessage):
#     def __init__(self, type, skip_checks=False, **kwargs):
#         super().__init__(type, skip_checks=False, **kwargs)

#         self.actual_time = 0

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
        f.write("\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n")


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
        self.message = mido.Message(type, **args)
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
            return f'Program change type: {self.type}, time: {self.time}, actual_time: {self.actual_time}'

class Note_rep:
    def __init__(self):
        self.type = ''
        self.channel=0
        self.note = ''
        self.velocity=0
        self.start_time=0
        self.duration=0
    
    def __init__(self, channel=0, note='', velocity=0, start_time=0, duration=0):
        self.channel=channel
        self.note = note
        self.velocity=velocity
        self.start_time=start_time
        self.duration=duration
    
    def __init__(self, obj: CustomMessage, duration=0): # use this
        self.type = 'note'
        if obj.type == 'note_on':
            self.channel = obj.channel
            self.note = obj.note
            self.velocity = obj.velocity
            self.start_time = obj.actual_time
            self.duration = duration
        else:
            self.type = 'not_note'

    def __init__(self, obj: CustomMetaMessage, duration=0): # we use the last two constructors
        self.type = 'not_note'
        self.channel = obj.channel
        self.note = obj.note
        self.velocity = obj.velocity
        self.start_time = obj.actual_time
        self.duration = duration

    def __str__(self):
        return f'type:{self.type} channel: {self.channel}, note: {self.note}, velocity: {self.velocity}, start_time: {self.start_time}, duration: {self.duration}'

LIM=10
#output intermediate
def conv_from_midi(track):
    global LIM
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
            if LIM >= 6:
                print('bak to they')
                LIM-=1
            custom_message = CustomMessage(msg.type)
            
            # Copy attributes from msg to custom_message
            custom_message.time = msg.time
            custom_message.actual_time = curr_time
            custom_message.velocity = msg.velocity  # Ensure velocity is copied correctly
            custom_message.note = msg.note          # Copy note if needed

            intermediate.append(custom_message)
        else:
            intermediate.append(msg)
    print_object_attributes(intermediate)
    for i in range(len(intermediate)):
        custom_msg=intermediate[i]
        
        if custom_msg.type=='note_on':
            # print(intermediate[i].type)
            print("-------")
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
                else:
                    # print('NOTA')
                    pass
                    # print(intermediate[j].velocity)
                    # print(intermediate[j].type)
    
    for line in intermediate:
        fwrite(line.__str__(), 'intermediate.txt')
    for line in desirable:
        fwrite(line.__str__(), 'desirable.txt')

    return desirable

def conv_to_midi(converted):
    pass


converted=conv_from_midi(midi_data.tracks[3])
print(len(converted))

f.close()