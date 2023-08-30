import rtmidi
import threading
import time
from rtmidi.midiconstants import (
    NOTE_ON,
    NOTE_OFF,
    PROGRAM_CHANGE
)

class CMidi:
    _instance = None  # Class level attribute to hold the singleton instance
    _initialized = False

    def __new__(cls, *args, **kwargs):
        # If an instance already exists, return that instance
        if not cls._instance:
            cls._instance = super(CMidi, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
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

    def _run(self):
        while self.running:
            with self.lock:
                if self.is_playing and self.to_play:
                    notes, velocity, channel = self.note_data
                    
                    # Check if the channel is valid
                    if channel not in range(16): 
                        channel = 0
                    
                    for note in notes:
                        self.send_note_on(note, velocity, channel)
                    
                    self.to_play = False
                        
                time.sleep(0.01)  # No tight loops, sleep for a brief moment

    def play_note(self, notes, velocity=100, channel=0):
        with self.lock:
            if not self.is_playing:
                self.is_playing = True
                self.to_play = True
                
                # Check if the channel is valid
                if channel not in range(16): 
                    channel = 0
                    
                self.note_data = (notes, velocity, channel)

    def stop_note(self):
        with self.lock:
            if self.is_playing:
                notes, _, channel = self.note_data
                for note in notes:
                    self.send_note_off(note, channel)
                self.is_playing = False  # Reset the state
                self.note_data = None

    def send_note_on(self, note, velocity, channel=0):
        note_on = [NOTE_ON + channel, note, velocity]
        self.midiout.send_message(note_on)

    def send_note_off(self, note, channel=0):
        note_off = [NOTE_OFF + channel, note, 0]
        self.midiout.send_message(note_off)
        
    def change_instrument(self, instrument, channel=0):
        """
        Change the instrument on a given channel.
        :param instrument: Instrument number (0-127)
        :param channel: MIDI channel (0-15)
        """
        if 0 <= instrument <= 127 and 0 <= channel <= 15:
            program_change = [PROGRAM_CHANGE + channel, instrument]
            self.midiout.send_message(program_change)
        else:
            print("Invalid instrument or channel number")

    def close(self):
        self.running = False
        self.thread.join()
        self.midiout.close_port()

if __name__ == "__main__":
    mm = CMidi()
    mm.change_instrument(19)
    mm.play_note([60], 112)  # Play middle C indefinitely
    time.sleep(1)
    mm.stop_note()
    mm.play_note([69,72,65], 112, 9)  # Sustain chord indefinitely
    time.sleep(3)
    mm.stop_note()  # Stop the indefinitely sustained note
    mm.play_note([60], 112, 1)  # Play middle C indefinitely
    time.sleep(2.2)
    mm.stop_note()

    mm.close()  # Close the MIDI connection
