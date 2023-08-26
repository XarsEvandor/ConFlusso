class CDummyControlDrums(object):
    def __init__(self):
       pass 
   
   
    def PlayNote1(self):
        oNote = CDummyNoteUnit()
        oNote.instrument = 1
        oNote.note = "C#"
        oNote.octave = 1
        oNote.play()
        print("Plays C in Minore Scale Note Unit")
                
        print("Plays Bass Drum Note Unit")   