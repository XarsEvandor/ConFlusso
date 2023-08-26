from ..MIDI import CMidi


class CDummyNoteUnit:
    def __init__(self, p_oControl, p_sNote=None):
        self.__note = None    
        
        self.control = p_oControl
        if p_sNote is not None:
            self.note = p_sNote
        self.midi = CMidi()
        self.duration = 5
        self.key = [60]
        self.instrument = 19
        
        
        
    @property
    def note(self):
        return self.__note
    
    @note.setter
    def note(self, p_sValue):
        self.__note = p_sValue
        if self.__note == "C":
            self.key = [60]
        elif self.__note == "C#":
            self.key = [63]
        
        
        
        
    def play(self):   
        nkey = self.key + (self.control.octave * 12)   
        self.midi.change_instrument(self.instrument)
        self.midi.play_note(nkey, 112) 
        self.midi.sleep(self.duration)
        self.midi.stop_note()


