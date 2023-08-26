from time import sleep
from . import CControlUnitBase
from . import CControlUnitClassic

import sys
print(sys.path)


class CGestureAssigner:
    def __init__(self):
        self._controlUnit = CControlUnitBase(None)
        self._controlUnitType = 0
        self._controlUnitTypes = [CControlUnitClassic]
        
        # Sets the control unit type to the first one in the list and creates an instance of it passing the previous control unit
        self._controlUnit = self._controlUnitTypes[self._controlUnitType](self._controlUnit)
        
        
    # ======= Right Hand =========
        
    def perform_right_hand_up_movement(self):
        self._controlUnit.PlayNote1()
        print("Note 1")
    
    def perform_right_hand_down_movement(self):
        self._controlUnit.PlayNote2()
        print("Note 2")
    
    def perform_right_hand_left_movement(self):
        self._controlUnit.PlayNote3()
        print("Note 3")
    
    def perform_right_hand_right_movement(self):
        self._controlUnit.PlayNote4()
        print("Note 4")
    
    def perform_right_hand_up_left_movement(self):
        self._controlUnit.PlayNote5()
        print("Note 5")
    
    def perform_right_hand_up_right_movement(self):
        self._controlUnit.PlayNote6()
        print("Note 6")
    
    def perform_right_hand_down_left_movement(self):
        self._controlUnit.PlayNote7()
        print("Note 7")
    
    def perform_right_hand_down_right_movement(self):
        self._controlUnit.PlayNote8()
        print("Note 8")
    
    def perform_right_hand_forward_movement(self):
        pass
    
    def perform_right_hand_backward_movement(self):
        pass
    
    def perform_right_hand_clockwise_rotation(self):
        pass
    
    def perform_right_hand_counter_clockwise_rotation(self):
        pass
    
    
    # ======= Left Hand =========
    
    def perform_left_hand_up_movement(self):
        self._controlUnit.ModifyTrack1()
        
    def perform_left_hand_down_movement(self):
        self._controlUnit.ModifyTrack2()
    
    def perform_left_hand_left_movement(self):
        self._controlUnit.ModifyTrack3()
    
    def perform_left_hand_right_movement(self):
        self._controlUnit.ModifyTrack4()
    
    def perform_left_hand_up_left_movement(self):
        self._controlUnit.ModifyTrack5()
    
    def perform_left_hand_up_right_movement(self):
        self._controlUnit.ModifyTrack6()
    
    def perform_left_hand_down_left_movement(self):
        self._controlUnit.ModifyTrack7()
    
    def perform_left_hand_down_right_movement(self):
        self._controlUnit.ModifyTrack8()
    
    def perform_left_hand_forward_movement(self):
        self._controlUnit.ModifyTrack9()
    
    def perform_left_hand_backward_movement(self):
        self._controlUnit.ModifyTrack10()
    
    def perform_left_hand_clockwise_rotation(self):
        self._controlUnit.ModifyTrack11()
    
    def perform_left_hand_counter_clockwise_rotation(self):
        # Switch control unit type
        index = (self._controlUnitType + 1) % len(self._controlUnitTypes)
        self._controlUnitType = index
        self._controlUnit = self._controlUnitTypes[index](self._controlUnit)
        
    
            
