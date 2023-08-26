from . import CControlUnitBase
   
class CControlUnitClassic(CControlUnitBase):
    def __init__(self, p_oPreviousControlUnit) -> None:
        super().__init__(p_oPreviousControlUnit) # call ancestral constructor
        
        #extra custom code 
        
    def ModifyTrack1(self):
        self._toggle_chord_mode()
        print("Chord mode toggled")
        
    def ModifyTrack2(self):
        self._cycle_chord_type_forward()
        print("Chord type cycled forward")
        
    def ModifyTrack3(self):
        self._cycle_chord_type_backward()
        print("Chord type cycled backward")
        
    def ModifyTrack4(self):
        self._octave_up()
        print("Octave up")
        
    def ModifyTrack5(self):
        self._octave_down()
        print("Octave down")
        
    def ModifyTrack6(self):
        self._play_percussion
        print("Switched to percussion channel")
        
    def ModifyTrack7(self):
        self._cycle_instrument_forward()
        print("Current instrument: " + self._instrument)
        
    def ModifyTrack8(self):
        self._cycle_instrument_backward()
        print("Current instrument: " + self._instrument)
        
    def ModifyTrack9(self):
        self._cycle_scales_forward()
        print("Changed to " + self._scale + " scale")
        
    def ModifyTrack10(self):
        self._cycle_scales_backward()
        print("Changed to " + self._scale + " scale")
        
    def ModifyTrack11(self):
        self._cycle_channel_forward()
        print("Switched to channel: " + str(self._channel))
        
        

class CControlUnitSpecial(CControlUnitClassic):
    def __init__(self, p_oPreviousControlUnit) -> None:
        super.__init__(p_oPreviousControlUnit)  # call ancestral constructor
        
        #extra custom code 
    
    def ModifyTrack1(self):
        self._toggle_chord_mode()
        print("Chord mode toggled")
        