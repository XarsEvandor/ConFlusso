from Assignment.NoteUnit import CNoteUnit


class CControlUnitBase:
    def __init__(self, p_oPreviousControlUnit) -> None:
        self._note = "C"
        self._octave = 0
        self._channel = 0
        self._velocity = 100

        self._allowed_instruments = [0, 33, 41, 43]
        self._instrument = self._allowed_instruments[0]

        self._chord_mode = False
        self._allowed_chord_types = [
            "major", "minor", "diminished", "augmented"]
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
        index = (self._allowed_chord_types.index(
            self._chord_type) + 1) % len(self._allowed_chord_types)
        self._chord_type = self._allowed_chord_types[index]

    def _cycle_chord_type_backward(self):
        index = (self._allowed_chord_types.index(
            self._chord_type) - 1) % len(self._allowed_chord_types)
        self._chord_type = self._allowed_chord_types[index]

    def _cycle_scales_forward(self):
        scale_keys = list(self._scales.keys())
        current_index = scale_keys.index(self._scale)
        next_index = (current_index + 1) % len(scale_keys)
        self._scale = scale_keys[next_index]

    def _cycle_scales_backward(self):
        scale_keys = list(self._scales.keys())
        current_index = scale_keys.index(self._scale)
        previous_index = (current_index - 1) % len(scale_keys)
        self._scale = scale_keys[previous_index]

    def _octave_up(self):
        self._octave += 1

    def _octave_down(self):
        self._octave -= 1

    def _octave_reset(self):
        self._octave = 0

    def _cycle_channel_forward(self):
        index = (self._channel + 1) % 4
        self._channel = index

    def _cycle_channel_backward(self):
        index = (self._channel - 1) % 4
        self._channel = index
        
    def _cycle_instrument_forward(self):
        index = (self._allowed_instruments.index(
            self._instrument) + 1) % len(self._allowed_instruments)
        self._instrument = self._allowed_instruments[index]
        self._cycle_channel_forward()

    def _cycle_instrument_backward(self):
        index = (self._allowed_instruments.index(
            self._instrument) - 1) % len(self._allowed_instruments)
        self._instrument = self._allowed_instruments[index]
        self._cycle_channel_backward()

    def _play_percussion(self):
        self._channel = 9
        ...

    def _get_note_by_position(self, position):
        current_scale = self._scales[self._scale]
        notes = list(current_scale.keys())
        return notes[position]

    def PlayNote1(self):
        self._note = self._get_note_by_position(0)  # First note in scale
        noteUnit = CNoteUnit(self)
        noteUnit.playNote()

    def PlayNote2(self):
        self._note = self._get_note_by_position(1)  # Second note in scale
        noteUnit = CNoteUnit(self)
        noteUnit.playNote()

    def PlayNote3(self):
        self._note = self._get_note_by_position(2)  # Third note in scale
        noteUnit = CNoteUnit(self)
        noteUnit.playNote()

    def PlayNote4(self):
        self._note = self._get_note_by_position(3)  # Fourth note in scale
        noteUnit = CNoteUnit(self)
        noteUnit.playNote()

    def PlayNote5(self):
        self._note = self._get_note_by_position(4)  # Fifth note in scale
        noteUnit = CNoteUnit(self)
        noteUnit.playNote()

    def PlayNote6(self):
        self._note = self._get_note_by_position(5)  # Sixth note in scale
        noteUnit = CNoteUnit(self)
        noteUnit.playNote()

    def PlayNote7(self):
        self._note = self._get_note_by_position(6)  # Seventh note in scale
        noteUnit = CNoteUnit(self)
        noteUnit.playNote()

    def PlayNote8(self):
        self._note = self._get_note_by_position(7)  # Eighth note in scale
        noteUnit = CNoteUnit(self)
        noteUnit.playNote()

    def StopNote(self):
        noteUnit = CNoteUnit(self)
        noteUnit.stop_note()

    def CloseMIDI(self):
        noteUnit = CNoteUnit(self)
        noteUnit.close_MIDI()

    def ModifyTrack1(self):
        pass  # custom action 1

    def ModifyTrack2(self):
        pass  # custom action 2

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

    def ModifyTrack9(self):
        pass

    def ModifyTrack10(self):
        pass

    def ModifyTrack11(self):
        pass
