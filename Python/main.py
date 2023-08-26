from Assignment import CGestureAssigner
from time import sleep


if __name__ == '__main__':
    assigner = CGestureAssigner()
    assigner.perform_right_hand_up_movement()
    sleep(secs=1)
    assigner.perform_right_hand_down_movement()
    sleep(secs=1)
    assigner.perform_left_hand_up_movement()
    assigner.perform_right_hand_down_movement()
    sleep(secs=1)
    assigner.perform_left_hand_right_movement()
    assigner.perform_right_hand_down_movement()
    sleep(secs=1)
