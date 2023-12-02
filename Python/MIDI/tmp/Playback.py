import mido
from mido import MidiFile
import threading
import time


class CPlayback:
    def __init__(self, midi_filename):
        self.midi_filename = midi_filename
        self.playing = False
        self.thread = None
        self.outport = mido.open_output()

    def _play_midi_loop(self):
        while self.playing:
            for msg in MidiFile(self.midi_filename).play():
                self.outport.send(msg)
            time.sleep(1)  # Sleep for 1 second before replaying

    def start_playback(self):
        if not self.playing:
            self.playing = True
            self.thread = threading.Thread(target=self._play_midi_loop)
            self.thread.start()

    def stop_playback(self):
        if self.playing:
            self.playing = False
            if self.thread:
                self.thread.join()
            self.outport.reset()

    def save_and_restart(self, new_midi_filename):
        self.stop_playback()
        # Here, you can add your logic to modify the MIDI file if needed
        self.midi_filename = new_midi_filename
        self.start_playback()


if __name__ == "__main__":
    player = CPlayback('output.mid')
    player.start_playback()
    time.sleep(10)  # Let it play for 10 seconds
    # Modify and restart with a new file
    player.save_and_restart('new_output.mid')
