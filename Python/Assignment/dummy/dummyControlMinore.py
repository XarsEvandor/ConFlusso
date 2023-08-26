class CDummyControlMinore(object):
    def __init__(self):
       self.octave = 1
       self.note_scale = CNoteControllerMinore(self)
   
    def ModifyTrack1(self):
        self.octave += 1
   
   
class CNoteControllerMinore(object):
    def __init__(self, p_oControl):
        self.control = p_oControl
        
    
    def PlayNote1(self):
        
        #CDummyNoteUnit(self.control, "C").play()
        
        oNote = CDummyNoteUnit(self.control)
        oNote.instrument = 19
        oNote.note = "C"
        oNote.octave = self.control.octave
        oNote.play()
        print("Plays C in Minore Scale Note Unit")
        
class CDummyNoteUnit:
    def __init__(self, p_oControl) -> None:
        self.control = p_oControl
    
    def play(self):
        self.instrument = 19
        self.note = "C"
        self..octave = self.control.octave

        print("Plays C in Minore Scale Note Unit")
        
        
    def play1(self.octave= 3):
        CMIDI.play_note([49,30,21])
                
    def play1(self.octave=2):
        CMIDI.play_note([50,30,21])