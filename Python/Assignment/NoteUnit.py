from MIDI.Midi import CMidi

class CNoteUnit:
    def __init__(self, control):
        self.control = control
        self.midi = CMidi()
        
    def create_chord(root_note, chord_type="major"):
        
        CHORD_PATTERNS = {
            "major": [0, 4, 7],          # Root, Major 3rd, Perfect 5th
            "minor": [0, 3, 7],          # Root, Minor 3rd, Perfect 5th
            "diminished": [0, 3, 6],     # Root, Minor 3rd, Diminished 5th
            "augmented": [0, 4, 8]       # Root, Major 3rd, Augmented 5th
        }

        # Fetch the pattern based on the chord type
        pattern = CHORD_PATTERNS.get(chord_type)

        # If the chord type isn't supported, raise an error
        if pattern is None:
            raise ValueError(f"Unsupported chord type: {chord_type}")

        # Construct the chord based on the root note and the pattern
        chord = [root_note + interval for interval in pattern]

        return chord
        
        
    def note_to_scale_key(self, scale :str = "Major" , note = "C") -> int:
        scale_notes = self.scales.get(scale)
        if not scale_notes:
            print(f"Scale {scale} not recognized. Defaulting to C Major.")
            scale_notes = self.control.scales[scale]

        self.key = [scale_notes.get(note, 60)]  # Default to C4 if note is not recognized
        
        
    def playNote(self):
        key = self.note_to_scale_key(self.control.scale, self.control.note)
        key = key + (self.control.octave * 12)
        if self.control.chord_mode:
            key = self.create_chord(key[0], self.control.chord_type)
        self.midi.change_instrument(self.control.instrument, self.control.channel)
        self.midi.play_note(key, self.control.velocity, self.control.channel)
        
        
        
        
        
        