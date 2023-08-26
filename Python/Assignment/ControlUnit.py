from . import NoteUnit

class  CControlUnitBase:
    def __init__(self, p_oPreviousControlUnit) -> None:
        self._note = "C"
        self._octave = 0
        self._channel = 0
        self._velocity = 100
        
        self._allowed_instruments = [0, 33, 41, 25]
        self._instrument = self._allowed_instruments[0]
        
        self._chord_mode = False
        self._allowed_chord_types = ["major", "minor", "diminished", "augmented"]
        self._chord_type = self._allowed_chord_types[0]
        
        self._scales = {
            "CMajor": {
                "C": 60, "D": 62, "E": 64, "F": 65, "G": 67, "A": 69, "B": 71, "high": 72
            },
            "Aminor": {
                "A": 69, "B": 71, "C": 60, "D": 62, "E": 64, "F": 65, "G": 67, "high": 81
            },
            "Cminor": {
                "C": 60, "D": 62, "Eb": 63, "F": 65, "G": 67, "Ab": 68, "Bb": 70, "high": 72
            }
        }
        
        self._scale = "CMajor"
        
        if p_oPreviousControlUnit is not None:
            self.merge_settings(p_oPreviousControlUnit)
                    
    def merge_settings(self, p_oPreviousControlUnit):
        self._note = p_oPreviousControlUnit._note
        self._octave = p_oPreviousControlUnit._octave
        self._channel = p_oPreviousControlUnit._channel
        self._velocity = p_oPreviousControlUnit._velocity
        
        self._instrument = p_oPreviousControlUnit._instrument
        
        self._chord_mode = p_oPreviousControlUnit._chord_mode 
        self._chord_type = p_oPreviousControlUnit._chord_type
        self._scale = p_oPreviousControlUnit._scale
        
    
    @property
    def velocity(self):
        return self._velocity
    
    @velocity.setter
    def velocity(self, velocity):
        self._velocity = velocity
        
    def _toggle_chord_mode(self):
        self._chord_mode = not self._chord_mode
        
    def _cycle_chord_type_forward(self):
        index = (self._allowed_chord_types.index(self._chord_type) + 1) % len(self._allowed_chord_types)
        self._chord_type = self._allowed_chord_types[index]
        
    def _cycle_chord_type_backward(self):
        index = (self._allowed_chord_types.index(self._chord_type) - 1) % len(self._allowed_chord_types)
        self._chord_type = self._allowed_chord_types[index]
        
    def _cycle_scales_forward(self):
        index = (self.scales.index(self._scale) + 1) % len(self.scales)
        self._scale = self.scales[index]
        
    def _cycle_scales_backward(self):
        index = (self.scales.index(self._scale) - 1) % len(self.scales)
        self._scale = self.scales[index]
        
    def _octave_up(self):
        self._octave += 1
    
    def _octave_down(self):
        self._octave -= 1
        
    def _octave_reset(self):
        self._octave = 0
    
    def _cycle_instrument_forward(self):
        index = (self._allowed_instruments.index(self._instrument) + 1) % len(self._allowed_instruments)
        self._instrument = self._allowed_instruments[index]
        
    def _cycle_instrument_backward(self):
        index = (self._allowed_instruments.index(self._instrument) - 1) % len(self._allowed_instruments)
        self._instrument = self._allowed_instruments[index]
            
    def _cycle_channel_forward(self):
        index = (self._channel + 1) % 16
        self._channel = index
        
        # Channel 9 is reserved for percussion
        if self._channel == 9:
            self._channel += 1
            
        # TODO: MIDI file is being scored while playing. When the channel changes, the file is closed, copied, and reopened. 
        # The copy of the midi file is then played on a separate thread. If a file is already playing, it should be closed and deleted.        
            
            
    def _cycle_channel_backward(self):
        index = (self._channel - 1) % 16
        self._channel = index
        
        # Channel 9 is reserved for percussion
        if self._channel == 9:
            self._channel -= 1
        
        
    def _play_percussion(self):
        self._channel = 9
        ...
        
        
        
    def PlayNote1(self):    
        self._note = "A"
        noteUnit = NoteUnit(self)
        noteUnit.playNote()
        
    def PlayNote2(self):
        self._note = "B"
        noteUnit = NoteUnit(self)
        noteUnit.playNote()
        
    def PlayNote3(self):
        self._note = "C"
        noteUnit = NoteUnit(self)
        noteUnit.playNote()
    
    def PlayNote4(self):
        self._note = "D"
        noteUnit = NoteUnit(self)
        noteUnit.playNote()
        
    def PlayNote5(self):
        self._note = "E"
        noteUnit = NoteUnit(self)
        noteUnit.playNote()
        
    def PlayNote6(self):
        self._note = "F"
        noteUnit = NoteUnit(self)
        noteUnit.playNote()
        
    def PlayNote7(self):
        self._note = "G"
        noteUnit = NoteUnit(self)
        noteUnit.playNote()
        
    def PlayNote8(self):
        self._note = "high"
        noteUnit = NoteUnit(self)
        noteUnit.playNote()
        
        

                
    def ModifyTrack1(self):
        pass # custom action 1
        
    def ModifyTrack2(self):
        pass # custom action 2
        
    def ModifyTrack3(self):
        pass
        
    def ModifyTrack4(self):
        pass
        
    def ModifyTrack5(self):
        pass
        
    def ModifyTrack6(self):
        pass
        
    def ModifyTrack7(self):
        pass
        
    def ModifyTrack8(self):
        pass
    
    def modifyTrack9(self):
        pass
    
    def modifyTrack10(self):
        pass
    
    def modifyTrack11(self):
        pass
    