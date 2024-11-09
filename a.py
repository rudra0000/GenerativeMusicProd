import mido
from extra import get_midi_duration


class note_rep:
    def __init__(self):
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
        pass
    
class CustomMessage(mido.messages.messages.Message):
    def __init__(self, type, extra_info=None, skip_checks=False, **args):
        # Call the parent constructor to set up the existing message structure
        super().__init__(type, skip_checks=skip_checks, **args)

        # Add the extra attribute
        self.time_actual = 0 # this is not delta time, it is the actual time



def pretty_print_arr(arr):
    print("[")
    for i in arr:
        print(i)
    print("]")

class Store:
    def __init__(self, mid):
        self.mid = mid
        self.tracks = mid.tracks
        self.ticks_per_beat = mid.ticks_per_beat
        flag  = False
        # find the tempo of the song
        for track in self.tracks:
            if flag:
                break
            for msg in track:
                if msg.type == 'set_tempo':
                    # print(msg)
                    self.tempo = msg.tempo # something like 352941 microseconds per beat
                    flag = True
                    break
        
        # turn all note_on events with velocity=0 to note_off events
        for track in self.tracks:
            if flag:
                break
            for i in range(len(track)):
                msg = track[i]
                if msg.type == 'note_on' and msg.velocity == 0:
                    msg.type = 'note_off'
                    track[i] = msg

    def print(self, i=None,msg_count=None):
        if i is None or msg_count is None:
            print('provide proper parameters')
        else:
            for j in range(msg_count):
                print(self.tracks[i][j])
    

    def get_ith_tracks_midi_file(self, i):
        ith_track = self.tracks[i]
        return ith_track
    
    def conv_to_my_notation(self,  track): # returns a new array with notes, start times and durations i.e. a conversion of the ith track
        # assume that the tempo of a piece is 120 BPM 
        # we will see messages like 
        # 1. note_on channel=0 note=50 velocity=50 time=0 # note that time here is delta time in some other unit not seconds
        # 2. program_change channel=0 program=0 time=0
        # 3. we need to convert this to an object and we can ignore note_off and program change events
        # the main challenge is that a note_on need not be followed immidiately by a note_off!!!!
        if track == None:
            print('will implement this later if needed')
            return
        ans = []
        cur_time = 0
        
        #first remove instead of time delta compute actual times
        f = open('a.txt', 'w')
        for i in range(0, len(track)):
            message = track[i]
            if message.is_meta or message.type == 'program_change':
                ans.append(message)
                continue # leave it unchanged

            elif message.type in ['note_on', 'note_off']:
                start_time = message.time + cur_time
                cur_time += message.time
                duration = 0
                # for j in range(i+1, len(track)):
                #     message2 = track[j]
                #     if message2.type == 'note_off' and message2.note == message.note:
                #         pass
                # note_rep(channel=message.channel, note=message.note, velocity=float(message.velocity), start_time=start_time, duration=duration)
                f.write(str(message) + "\n")
                f.write(str(type(message)))
                pass
            else:
                print(message, 'I do not like this')

        return ans

        pass

    def conv_to_original_notation(self, track):
        ans = []
        if track is None:
            print('will be implemented later')
            return
        else:
            for j in range (len(track)):
                message = track[j]
                if j > 0:
                    prev_message = track[j-1]
                # print('---------------', 'message is', message)
                # print('the type(message) gives', type(message))
                if isinstance(message, (mido.messages.messages.Message, mido.midifiles.meta.MetaMessage)):
                    ans.append(message)
                elif message['type'] != 'note_on':
                    ans.append(message)
                else:
                    new_message = {}
                    new_message['type']=message['type']
                    new_message['velocity']=message['velocity']
                    if j == 0:
                        new_message['time'] = message['start_time']
                    else:
                        if isinstance(prev_message, (mido.messages.messages.Message)):
                            req_start_time = prev_message.time
                        else:
                            req_start_time = prev_message['start_time']
                        new_message['time'] = message['start_time'] - req_start_time
                    new_message2 = {}
                    new_message2['type'] = 'note_off'
                    new_message2['velocity'] = 0
                    new_message2['start_time'] = message['start_time'] + message['duration']
                    new_message['note'] = message['note']
                    new_message2['note'] = message['note']
                    new_message['channel'] = message['channel']
                    new_message2['channel'] = message['channel']
                    ans.append(new_message)
                    ans.append(new_message2)
        return ans
        pass


POPULATION_SIZE = 20

#based on the initial song, we need to get a population


mid = mido.MidiFile('./midi_files/FOB_swgd.mid')
store = Store(mid)

i=0
end=15

print('ith track is:')
# print(store.tracks[i])

print(store.tracks[i][0:end])
print('-------------------------------------------')
x = store.conv_to_my_notation(store.tracks[i])
# pretty_print_arr(x[0:end])
# print('-------------------------------------------')
# y = store.conv_to_original_notation(x)
# pretty_print_arr(y[0:end])
# print('-------------------------------------------')








def experiment1():
    # Load the MIDI file
    file_path = './midi_files/FOB_swgd.mid'
    mid = mido.MidiFile(file_path)
    print('duration is', get_midi_duration(mid), 'seconds')
    store = Store(mid)

    # let's try to create a new midi file using only the ith track of the old one
    i=1
    req_track = store.get_ith_tracks_midi_file(i)

    new_track_messages  = []
    for msg in req_track:
        new_track_messages.append(msg)


    new_mid = mido.MidiFile()
    new_mid.add_track('track0')
    new_mid.tracks[0] += new_track_messages
    # print(new_mid.tracks)


    new_mid.save('./midi_files/new.mid')




# experiment1()





