import rtmidi as midi

# create static midi class that can be used to send midi messages
class CMidi:
    # constructor
    
    
    def playNoteOn(self, note, velocity):
        self.midiout.send_message([0x90, note, velocity])
    
    