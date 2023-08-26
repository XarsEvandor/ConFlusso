class CDummyAssigner(object):
    def __init__(self):
       self.control_unit = CDummyControlDrums()
       
    def switch_to_minore(self):
        self.control_unit = CDummyControlMinore()
        
    def switch_to_drums(self):
        self.control_unit = CDummyControlDrums()
        
        
        
    def PlayGestureLeft(self):
        pass
    def PlayGestureUp(self):
        self.control_unit.note_scale.PlayNote2()
    def PlayGestureRight(self):
        pass
    def PlayGesture4(self):
        pass
    def PlayGesture5(self):
        pass
    def PlayGesture6(self):
        pass
    def PlayGesture7(self):
        pass
    def PlayGesture8(self):
        pass              
    
    def PlayGesture9(self):
        pass
    
    def PlayGesture10(self):
        self.control_unit.ModifyTrack2()
    def PlayGesture11(self):
        pass
    def PlayGesture12(self):
        pass
    def PlayGesture13(self):
        pass
    def PlayGesture14(self):
        pass
    def PlayGesture15(self):
        pass
    def PlayGesture16(self):
        pass       
    