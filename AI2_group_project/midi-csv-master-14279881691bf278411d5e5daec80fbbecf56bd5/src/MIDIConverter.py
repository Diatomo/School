import sys
from mido import MidiFile
from mido import MidiTrack
from mido import Message
from mido import MetaMessage
from mido import tick2second
from mido import second2tick


class NoteParser:
    def __init__(self, mid, ticks_per_beat, sampling_t, rows):
        self.active_notes = [None] * 127
        self.sampling_t = sampling_t
        self.file = open(mid.filename[:-4] + '.csv', 'w')
        self.mid = mid
        self.trim_whitespace(mid)
        self.tempo = 512810
        self.ticks_per_beat = ticks_per_beat
        self.ms_per_row = self.s2ms(mid.length / rows)
        self.writes_per_row = self.s2ms((mid.length / rows)) / sampling_t
        self.rows = rows

        self.writes = 0
        self.tot_writes = 0

    # write active notes to a csv file.  Logic to limit row numbers is here
    def write_csv(self):
        self.writes += 1

        if (self.writes * self.sampling_t) % self.ms_per_row < self.sampling_t and self.tot_writes < self.rows:
            self.write_row()

    # writes a row to the csv file
    def write_row(self):
        row = ''
        for note in self.active_notes:
            if note is not None:
                row += str(note)
            else:
                row += '0'
            row += ','
        # remove the last comma cause baylife (haha like bayless)
        row = row[:-1]
        self.file.write(row + '\n')
        self.tot_writes += 1

    # parse note_on messages
    def parse_note_on(self, msg):
        self.active_notes[msg.note] = msg.velocity
        return

    # parse note_off messages
    def parse_note_off(self, msg):
        self.active_notes[msg.note] = None
        return

    # parse control_change messages (set_tempo)
    def parse_control_change(self, msg):
        # for now, ignore, idk what they do
        return

    # parses meta messags
    def parse_meta_msg(self, msg):
        if msg.type == 'set_tempo':
            self.set_tempo(msg.tempo)

    def parse_note(self, msg):
        if msg.type == 'note_on':
            self.parse_note_on(msg)
        elif msg.type == 'note_off':
            self.parse_note_off(msg)
        elif msg.type == 'control_change':
            self.parse_control_change(msg)
        elif msg.is_meta:
            self.parse_meta_msg(msg)
        return

    def seconds2ticks(self, seconds):
        return second2tick(seconds, self.ticks_per_beat, self.tempo)

    def ticks2seconds(self, ticks):
        return tick2second(ticks, self.ticks_per_beat, self.tempo)

    def close(self):
        self.file.close()

    def set_tempo(self, tempo):
        self.tempo = tempo

    def end_file(self):
        row = ''
        for note in self.active_notes:
            row += '0,'
        row = row[:-1]

    def parse(self):
        notes = list(self.mid.tracks[0])
        time_elapsed = 0
        tot_time = 0
        tot_ticks = 0

        while len(notes) > 0:
            time = time_elapsed
            time_elapsed += self.seconds2ticks(self.ms2s(self.sampling_t))

            tot_time += self.ms2s(self.sampling_t)

            current_note = notes[0]
            while current_note.time <= time and len(notes) > 0:
                self.parse_note(current_note)

                tot_ticks += current_note.time

                notes.pop(0)
                if len(notes) > 0:
                    current_note = notes[0]

                time = 0
                time_elapsed = 0
            self.write_csv()

        self.end_file()

        print 'total rows ' + str(self.tot_writes)

    # trims whitespace from midi file by removing last meta messages from song
    @staticmethod
    def trim_whitespace(mid):
        notes = mid.tracks[0]
        i = -1
        current_note = notes[i]
        while current_note.type != 'note_on' and current_note.type != 'note_off':
            current_note.time = 0
            current_note = notes[i - 1]
            i = i - 1
        return

    @staticmethod
    def ms2s(ms):
        return ms / 1000.

    @staticmethod
    def s2ms(s):
        return s * 1000


class CSVParser:

    def __init__(self, csv_file, deltaT):
        self.deltaT = deltaT
        self.csv_file = csv_file
        # default values cause yolo
        self.ticks_per_beat = 384
        self.tempo = 512820
        self.active_notes = [None] * 127
        self.mid = MidiFile(ticks_per_beat=self.ticks_per_beat)
        self.track = MidiTrack()
        self.mid.tracks.append(self.track)
        self.set_meta_tempo()
        self.last_note_time = 0

    def set_tempo(self, tempo):
        self.tempo = tempo

    def ms2sec(self, ms):
        return self.deltaT / 1000.

    def seconds2ticks(self, seconds):
        return second2tick(seconds, self.ticks_per_beat, self.tempo)

    def ticks2seconds(self, ticks):
        return tick2second(ticks, self.ticks_per_beat, self.tempo)

    def parse_row(self, row, index):
        notes = row.split(',')
        notes = map(int, notes)
        is_first = True
        for i in range(0, len(notes)):
            if notes[i] != 0:
                if self.active_notes[i] is None:
                    self.active_notes[i] = True
                    ticks = 0
                    if is_first:
                        ticks = self.seconds2ticks(index * self.ms2sec(self.deltaT)) - self.last_note_time
                        self.last_note_time = self.seconds2ticks(index * self.ms2sec(self.deltaT))
                        is_first = False
                    self.note_on(i, notes[i], int(ticks))
            else:
                if self.active_notes[i]:
                    ticks = 0
                    if is_first:
                        ticks = self.seconds2ticks(index * self.ms2sec(self.deltaT)) - self.last_note_time
                        self.last_note_time = self.seconds2ticks(index * self.ms2sec(self.deltaT))
                        is_first = False
                    self.note_off(i, int(ticks))
                    self.active_notes[i] = None

    def set_last_note(self,ticks):
        self.last_note_time = ticks

    def note_on(self, note, intensity, delta_ticks):
        self.track.append(Message('note_on', note=note, velocity=intensity, time=delta_ticks))

    def note_off(self, note, delta_ticks):
        self.track.append(Message('note_off', note=note, velocity=64, time=delta_ticks))

    def set_meta_tempo(self):
        self.track.append(MetaMessage('set_tempo', tempo=self.tempo))

    def convert(self):
        with open(self.csv_file, 'r') as f:
            i = 0
            for line in f:
                self.parse_row(line, i)
                i += 1


    def save(self):
        self.mid.save(self.csv_file[:-4] + 'FromCSV.mid')


def midi_to_csv(midi_file, sampling_t, output_t):
    mid = MidiFile(midi_file)
    parser = NoteParser(mid, mid.ticks_per_beat, sampling_t, output_t)
    parser.parse()


def csv_to_midi(csv_file, deltaT):
    csvParser = CSVParser(csv_file, deltaT)
    csvParser.convert()
    csvParser.save()
    return

def get_initial_tempo(parser, mid):
    notes = mid.tracks[0]
    tempos = filter(lambda x: x.type == 'set_tempo', notes)
    if len(tempos) > 0:
        parser.set_tempo(tempos.tempo)




if __name__ == '__main__':
    if len(sys.argv) != 4 and len(sys.argv) != 5:
        print 'invalid number of arguments'
        sys.exit()

    # mc converts midi to csv, cm does csv to midi
    # mc args file_name sampling rate in ms num_rows
    # cm args file_name sampling rate
    if sys.argv[1] == '-mc':
        midi_to_csv(sys.argv[2], float(sys.argv[3]), float(sys.argv[4]))
    elif sys.argv[1] == '-cm':
        csv_to_midi(sys.argv[2], float(sys.argv[3]))
    else:
        print 'invalid argument + \'' + sys.argv[1] + '\''
        sys.exit()
