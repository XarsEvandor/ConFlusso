import os
import pandas as pd
import json

class GestureRecognizer:
    def __init__(self, json_file, window_size=5, mode='full_mobility'):
        self.mode = mode
        self.thresholds = self.load_thresholds(json_file)
        self.window_size = window_size
        self.current_state = "Centered"
        self.last_gesture = None

    def load_thresholds(self, json_file):
        with open(json_file, 'r') as file:
            data = json.load(file)
        thresholds = data[self.mode][0]
        return thresholds

    def opposite_gesture(self, gesture):
        opposites = {
            'up': 'down',
            'down': 'up',
            'left': 'right',
            'right': 'left',
            'clockwise': 'counter_clockwise',
            'counter_clockwise': 'clockwise'
        }
        return opposites.get(gesture)

    def detect_gesture(self, data_samples):
        if len(data_samples) < self.window_size:
            return "Centered", None  # Default to "Centered" if not enough samples

        # Convert to DataFrame
        df = pd.DataFrame(data_samples)

        # Calculate deltas within the window
        roll_delta = df['Roll'].iloc[-1] - df['Roll'].iloc[0]
        pitch_delta = df['Pitch'].iloc[-1] - df['Pitch'].iloc[0]
        heading_delta = df['Heading'].iloc[-1] - df['Heading'].iloc[0]

        # Determine new potential gesture based on deltas
        new_gesture = None  
        if roll_delta >= self.thresholds['roll_threshold_up']:
            new_gesture = 'up'
        elif roll_delta <= self.thresholds['roll_threshold_down']:
            new_gesture = 'down'
        elif heading_delta <= self.thresholds['heading_threshold_left']:
            new_gesture = 'left'
        elif heading_delta >= self.thresholds['heading_threshold_right']:
            new_gesture = 'right'
        elif pitch_delta >= self.thresholds['pitch_threshold_clockwise']:
            new_gesture = 'clockwise'
        elif pitch_delta <= self.thresholds['pitch_threshold_counterclockwise']:
            new_gesture = 'counter_clockwise'

        # Gesture detection and state management
        if self.current_state == "Centered":
            if new_gesture is not None:
                self.current_state = new_gesture
                self.last_gesture = new_gesture
        elif self.current_state in ["up", "down", "left", "right", "clockwise", "counter_clockwise"]:
            if new_gesture == self.opposite_gesture(self.current_state):
                self.current_state = "Transition"
        elif self.current_state == "Transition":
            if new_gesture is None:
                self.current_state = "Centered"

        # Log the last stable gesture during transition, and "Centered" when transition is complete
        gesture_detected = self.last_gesture if self.current_state != "Centered" else "Centered"

        return df, {
            'Roll_Delta': roll_delta,
            'Pitch_Delta': pitch_delta,
            'Heading_Delta': heading_delta
        }, gesture_detected

def process_data(input_file, output_file, json_file, log_file):
    recognizer = GestureRecognizer(json_file)
    data = pd.read_csv(input_file)
    results = []
    log = []

    for i in range(len(data) - recognizer.window_size + 1):
        sample = data.iloc[i:i+recognizer.window_size]
        window, deltas, gesture = recognizer.detect_gesture(sample)
        timestamp = window.iloc[-1]['Timestamp']
        if gesture is not None and recognizer.current_state != "Transition":
            results.append({'Timestamp': timestamp, 'Gesture': gesture})
        log.append({
            'Timestamp': timestamp, 
            'Roll_Delta': deltas['Roll_Delta'], 
            'Pitch_Delta': deltas['Pitch_Delta'], 
            'Heading_Delta': deltas['Heading_Delta'],
            'Detected_Gesture': gesture if recognizer.current_state != "Transition" else recognizer.last_gesture,
            'Actual_Roll': window['Roll'].tolist(),
            'Actual_Pitch': window['Pitch'].tolist(),
            'Actual_Heading': window['Heading'].tolist()
        })

    pd.DataFrame(results).to_csv(output_file, index=False)
    pd.DataFrame(log).to_csv(log_file, index=False)

# Example usage
script_dir = os.path.dirname(os.path.realpath(__file__))  # Get the directory of the script
input_file_path = os.path.join(script_dir, "orientation_data.csv")
output_file_path = os.path.join(script_dir, "gesture_results.csv")
json_file_path = os.path.join(script_dir, "recognition_profiles.json")
log_file_path = os.path.join(script_dir, "gesture_log.csv")
process_data(input_file_path, output_file_path, json_file_path, log_file_path)
 