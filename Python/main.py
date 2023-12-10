import datetime
import json
import subprocess
import time
from Assignment.GestureAssigner import CGestureAssigner
from MIDI.Midi import CMidi
from time import sleep
import keyboard
import threading

def listen_for_gesture_changes():
    while not exit_flag.is_set():
        # Block until a key is pressed
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            update_control_gesture(event.name)

def update_control_gesture(key):
    def close_midi_and_set_exit_flag():
        assigner.perform_left_hand_counter_clockwise_rotation()
        exit_flag.set()
        global event_counter
        
        if event_counter > 20:
            try:
                subprocess.run(["python", "ML\\Local_Allegro\\allegro_single_script.py"], check=True)
                exit(0)
            except subprocess.CalledProcessError as e:
                print(f"Failed to run allegro_script.py: {e}")
        else:
            print("Not enough events to generate music")
        
    gesture_mapping = {
            'num 1': assigner.perform_left_hand_up_movement,  # Toggles chord mode
            'num 2': assigner.perform_left_hand_down_movement,  # Cycles chord type forward
            'num 3': assigner.perform_left_hand_left_movement,  # Cycles chord type backward
            'num 4': assigner.perform_left_hand_right_movement,  # Octave up
            'num 5': assigner.perform_left_hand_up_left_movement,  # Octave down
            'num 6': assigner.perform_left_hand_down_left_movement,  # Cycles instrument forward
            'num 7': assigner.perform_left_hand_down_right_movement,  # Cycles instrument backward
            'num 8': assigner.perform_left_hand_forward_movement,  # Cycles scales forward
            'num 9': assigner.perform_left_hand_backward_movement,  # Cycles scales backward
            '/': close_midi_and_set_exit_flag  # Close MIDI
    }
    if key in gesture_mapping:
        gesture_mapping[key]()

def play_sequence():
    global event_counter
    midi = CMidi()
    
    while not exit_flag.is_set():
        assigner.perform_right_hand_up_movement()  # C
        gesture_time = datetime.datetime.now().microsecond
        sound_time = midi.time_millis
        
        delay = sound_time - gesture_time
        print(f"Gestured at: {gesture_time} μs")
        print(f"Sound at: {sound_time} μs")
        print(f"Delay: {delay} μs")
            
        sleep(0.5)
        assigner.perform_right_hand_centered()

        assigner.perform_right_hand_down_movement()  # D
        sleep(0.5)
        assigner.perform_right_hand_centered()

        assigner.perform_right_hand_left_movement()  # E
        sleep(0.5)
        assigner.perform_right_hand_centered()

        assigner.perform_right_hand_up_left_movement()  # G
        sleep(0.5)
        assigner.perform_right_hand_centered()

        assigner.perform_right_hand_up_right_movement()  # A
        sleep(0.5)
        assigner.perform_right_hand_centered()

        assigner.perform_right_hand_up_movement()  # C
        sleep(1)
        assigner.perform_right_hand_centered()
        if exit_flag.is_set():
            break

        # Repeat
        assigner.perform_right_hand_down_left_movement()  # B
        sleep(0.5)
        assigner.perform_right_hand_centered()
        
        assigner.perform_right_hand_down_movement()  # D
        sleep(0.5)
        assigner.perform_right_hand_centered()

        assigner.perform_right_hand_left_movement()  # E
        sleep(0.5)
        assigner.perform_right_hand_centered()

        assigner.perform_right_hand_up_left_movement()  # G
        sleep(0.5)
        assigner.perform_right_hand_centered()

        assigner.perform_right_hand_up_right_movement()  # A
        sleep(0.5)
        assigner.perform_right_hand_centered()

        assigner.perform_right_hand_down_right_movement()  # High C
        sleep(1)
        assigner.perform_right_hand_centered()
        
        event_counter += 12
        if exit_flag.is_set():
            break

if __name__ == '__main__':
    assigner = CGestureAssigner()
    exit_flag = threading.Event()
    event_counter = 0

    for key in ['num 1', 'num 2', 'num 3', 'num 4', 'num 5', 'num 6', 'num 7', 'num 8', 'num 9', 'num 0', '*', '/']:
        keyboard.on_press_key(key, lambda e, key=key: update_control_gesture(key))

    sequence_thread = threading.Thread(target=play_sequence)
    sequence_thread.start()

    try:
        while not exit_flag.is_set():
            sleep(0.1)  
    except KeyboardInterrupt:
        exit_flag.set()

    sequence_thread.join()
    keyboard.unhook_all()

    exit(0)