import mido

FILENAME = './duckandrun.mid'
midi_data = mido.MidiFile(filename=f'./midi_files/{FILENAME}')
midi_track0 = midi_data.tracks[0]

def fwrite(str1, filename):
    with open(filename, 'a') as f:
        f.write(str1 + "\n")

f = open("intermediate.txt", "w")

def print_object_attributes(objects):
    for obj in objects:
        attributes = vars(obj)
        f.write(" | ".join(f"{key}={value}" for key, value in attributes.items()))
        f.write("\n")

class CustomMetaMessage:
    def __init__(self, type, skip_checks=False, **kwargs):
        self.meta_message = mido.MetaMessage(type, skip_checks=skip_checks, **kwargs)
        self.actual_time = 0

    def __getattr__(self, name):
        return getattr(self.meta_message, name)

    def __setattr__(self, name, value):
        if name != "meta_message" and name != "actual_time":
            setattr(self.meta_message, name, value)
        else:
            super().__setattr__(name, value)

    def __str__(self):
        return f'MetaMessage type: {self.type}, time: {self.time}, actual_time: {self.actual_time}'

class CustomMessage:
    def __init__(self, type, skip_checks=False, extra_info=None, **args):
        self.message = mido.messages.messages.Message(type, **args)
        self.actual_time = 0

    def __getattr__(self, name):
        return getattr(self.message, name)

    def __setattr__(self, name, value):
        if name not in ['message', 'actual_time']:
            setattr(self.message, name, value)
        else:
            super().__setattr__(name, value)
    
    def __str__(self):
        if self.type == 'note_on':
            return f'Message(notes) type: {self.type}, time: {self.time}, actual_time: {self.actual_time}, note: {self.note}, velocity: {self.velocity}'
        else:
            return f'Program change type: {self.type}, time: {self.time}, actual_time: {self.actual_time}'

class Note_rep:
    def __init__(self, obj, duration=0):
        self.type = 'note'
        self.obj = obj
        if obj.type == 'note_on':
            self.channel = obj.channel
            self.note = obj.note
            self.velocity = obj.velocity
            self.actual_time = obj.actual_time
            self.duration = duration
        else:
            self.type = 'not_note'
            self.obj = obj

    def __str__(self):
        if self.type == 'note':
            return f'type:{self.type} channel: {self.channel}, note: {self.note}, velocity: {self.velocity}, actual_time: {self.actual_time}, duration: {self.duration}'      
        else:
            return f'type: {self.type}, obj: {self.obj}'

LIM = 10

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
                LIM -= 1
            custom_message = CustomMessage(msg.type)
            custom_message.time = msg.time
            custom_message.actual_time = curr_time
            custom_message.velocity = msg.velocity
            custom_message.note = msg.note
            intermediate.append(custom_message)
        else:
            intermediate.append(msg)
    print_object_attributes(intermediate)
    
    for i in range(len(intermediate)):
        custom_msg = intermediate[i]
        if custom_msg.type == 'note_on':
            for j in range(i + 1, len(intermediate)):
                higher_lvl_message = intermediate[j]
                condition1 = (isinstance(intermediate[j], CustomMessage)) and (higher_lvl_message.type == 'note_off') and (higher_lvl_message.note == custom_msg.note)
                condition2 = (higher_lvl_message.type == 'note_on') and (higher_lvl_message.note == custom_msg.note) and (higher_lvl_message.velocity == 0)
                if condition1 or condition2:
                    duration = intermediate[j].actual_time - custom_msg.actual_time
                    note_rep = Note_rep(custom_msg, duration=duration)
                    desirable.append(note_rep)
                    break
        else:
            note_rep = Note_rep(custom_msg, duration=0)
            desirable.append(note_rep)

    for line in intermediate:
        fwrite(line.__str__(), 'intermediate.txt')
    for line in desirable:
        fwrite(line.__str__(), 'desirable.txt')

    return desirable

def save_track_to_midi(track2, output_file_path, tempo):
    global midi_track0
    midi = mido.MidiFile()
    midi_track = mido.MidiTrack()
    midi.tracks.append(midi_track0)
    midi.tracks.append(midi_track)
    
    midi_track.append(mido.MetaMessage('set_tempo', tempo=tempo))
    
    for msg in track2:
        if isinstance(msg, mido.MetaMessage):
            midi_track.append(msg)
        elif isinstance(msg, mido.messages.messages.Message):
            midi_track.append(msg)
        else:
            print(f"Skipping unknown message type: {msg}")

    midi.save(output_file_path)
    print(f"MIDI file saved to {output_file_path}")

def conv_to_midi(converted, tempo):
    intermediate2 = []
    for note_rep in converted:
        if note_rep.type == 'note':
            note_on = CustomMessage('note_on', channel=note_rep.channel, note=note_rep.note, velocity=note_rep.velocity, time=note_rep.actual_time)
            note_off = CustomMessage('note_off', channel=note_rep.channel, note=note_rep.note, velocity=0, time=note_rep.actual_time + note_rep.duration)
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
    
    save_track_to_midi(track2, 'output.mid', tempo)
    return track2

# Get tempo from the first track
for msg in midi_data.tracks[0]:
    if msg.type == 'set_tempo':
        input_tempo = msg.tempo
        break

converted = conv_from_midi(midi_data.tracks[1])
track2 = conv_to_midi(converted, input_tempo)
print(len(converted))

track = midi_data.tracks[1]
save_track_to_midi(track, 'input.mid', input_tempo)

f.close()
      
