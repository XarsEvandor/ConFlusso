import rtmidi
import threading
from .CScorer import CScorer

import time
from rtmidi.midiconstants import (
    NOTE_ON,
    NOTE_OFF,
    PROGRAM_CHANGE
)


class CMidi:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(CMidi, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.start_time = time.time()
            self.midiout = rtmidi.MidiOut()
            available_ports = self.midiout.get_ports()
            if available_ports:
                self.midiout.open_port(0)
            else:
                print("No MIDI port found")

            self.is_playing = False
            self.to_play = False
            self.lock = threading.Lock()
            self.note_data = None

            self.running = True
            self.thread = threading.Thread(target=self._run)
            self.thread.start()
            CMidi._initialized = True

            self.scorer = CScorer()  # Create a CScorer instance

    def _get_elapsed_time(self):
        return time.time() - self.start_time

    def _run(self):
        while self.running:
            with self.lock:
                if self.is_playing and self.to_play:
                    notes, velocity, channel = self.note_data
                    if channel not in range(16):
                        channel = 0
                    for note in notes:
                        self.send_note_on(note, velocity, channel)
                    self.to_play = False
                time.sleep(0.01)

    def play_note(self, notes, velocity=100, channel=0):
        with self.lock:
            if not self.is_playing:
                self.is_playing = True
                self.to_play = True
                if channel not in range(16):
                    channel = 0
                self.note_data = (notes, velocity, channel)
                elapsed_time = self._get_elapsed_time()
                for note in notes:
                    self.scorer.log_note(note, elapsed_time)

    def stop_note(self):
        with self.lock:
            if self.is_playing:
                notes, _, channel = self.note_data
                elapsed_time = self._get_elapsed_time()
                for note in notes:
                    self.send_note_off(note, channel)
                    self.scorer.log_note_off(note, elapsed_time)
                self.is_playing = False
                self.note_data = None

    def send_note_on(self, note, velocity, channel=0):
        note_on = [NOTE_ON + channel, note, velocity]
        self.midiout.send_message(note_on)

    def send_note_off(self, note, channel=0):
        note_off = [NOTE_OFF + channel, note, 0]
        self.midiout.send_message(note_off)

    def change_instrument(self, instrument, channel=0):
        if 0 <= instrument <= 127 and 0 <= channel <= 15:
            program_change = [PROGRAM_CHANGE + channel, instrument]
            self.midiout.send_message(program_change)
        else:
            print("Invalid instrument or channel number")

    def close(self):
        self.running = False
        self.thread.join()
        self.midiout.close_port()

    def save_midi_file(self, filename):
        self.scorer.save_midi(filename)


if __name__ == "__main__":
    mm = CMidi()
    mm.change_instrument(19)
    mm.play_note([60], 112)
    time.sleep(1)
    mm.stop_note()
    mm.play_note([69, 72, 65], 112, 9)
    time.sleep(3)
    mm.stop_note()
    mm.play_note([60], 112, 1)
    time.sleep(2.2)
    mm.stop_note()
    mm.save_midi_file('output.mid')
    mm.close()
