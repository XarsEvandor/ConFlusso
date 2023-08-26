from mido import MidiFile, MidiTrack, Message

# SAMPLE USAGE
# scorer = CScorer()
# scorer.log_note(60, 0.5)

class CScorer:
    def __init__ (self, ticks_per_beat = 480):
        self.mid = MidiFile(ticks_per_beat = ticks_per_beat)
        self.track = MidiTrack()
        self.mid.tracks.append(self.track)
        self.prev_timestamp = None
        
    def _elapsed_time_to_ticks(self, elapsed_time):
        return int(elapsed_time * self.mid.ticks_per_beat)      

    def log_note(self, note, elapsed_seconds, message_type='note_on', velocity=60):
        ticks_since_last_note = self._elapsed_time_to_ticks(elapsed_seconds)
        self.track.append(Message(message_type, note=note, velocity=velocity, time=ticks_since_last_note))
        
    def add_track(self, track):
        self.mid.tracks.append(track)
        
    def save_midi(self, filename):
        self.mid.save(filename)
    
    def edit_midi(self, filename):
        self.mid = MidiFile(filename)
        
        # Remove the last track
        if self.mid.tracks:
            del self.mid.tracks[-1]
            
        self.mid.save(filename)
        
    
    