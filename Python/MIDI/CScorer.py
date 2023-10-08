from mido import MidiFile, MidiTrack, Message
import rtmidi
import threading
import time
from rtmidi.midiconstants import (
    NOTE_ON,
    NOTE_OFF,
    PROGRAM_CHANGE
)


class CScorer:
    def __init__(self, ticks_per_beat=480):
        self.last_logged_time = 0
        self.mid = MidiFile(ticks_per_beat=ticks_per_beat)
        self.track = MidiTrack()
        self.mid.tracks.append(self.track)
        self.prev_timestamp = 0  # Set to 0 initially

    def _elapsed_time_to_ticks(self, elapsed_time):
        return int(elapsed_time * self.mid.ticks_per_beat)

    def log_note(self, note, elapsed_seconds, message_type='note_on', velocity=60):
        time_difference = elapsed_seconds - self.last_logged_time
        ticks_since_last_note = self._elapsed_time_to_ticks(time_difference)
        self.track.append(Message(message_type, note=note,
                          velocity=velocity, time=ticks_since_last_note))
        self.last_logged_time = elapsed_seconds

    def log_note_off(self, note, elapsed_seconds):
        time_difference = elapsed_seconds - self.last_logged_time
        ticks_since_last_note = self._elapsed_time_to_ticks(time_difference)
        self.track.append(Message('note_off', note=note,
                          velocity=0, time=ticks_since_last_note))
        self.last_logged_time = elapsed_seconds

    def add_track(self, track):
        self.mid.tracks.append(track)

    def save_midi(self, filename):
        try:
            self.mid.save(filename)
            print(f'MIDI file saved as {filename}')
        except Exception as e:
            print(f'Failed to save MIDI file: {e}')

    def edit_midi(self, filename):
        try:
            self.mid = MidiFile(filename)
        except Exception as e:
            print(f'Failed to edit MIDI file: {e}')
            return

        # Remove the last track
        if self.mid.tracks:
            del self.mid.tracks[-1]

        try:
            self.mid.save(filename)
            print(f'MIDI file edited and saved as {filename}')
        except Exception as e:
            print(f'Failed to save edited MIDI file: {e}')
