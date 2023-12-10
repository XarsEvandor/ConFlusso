import mido
from mido import MidiFile
import threading
import time

class CPlayback:
    def __init__(self, midi_filename, outport = mido.open_output()):
        self.midi_filename = midi_filename
        self.playing = False
        self.thread = None
        self.lock = threading.Lock()
        self.outport = outport
    def _play_midi_loop(self):
        try:
            midi = MidiFile(self.midi_filename)
            while True:
                with self.lock:
                    if not self.playing:
                        break
                for msg in midi.play():
                    with self.lock:
                        if not self.playing:
                            return
                        self.outport.send(msg)
                time.sleep(1)  # Sleep for 1 second before replaying
        except Exception as e:
            print(f"Error in playback thread: {e}")

    def start_playback(self):
        with self.lock:
            if not self.playing:
                self.playing = True
                self.thread = threading.Thread(target=self._play_midi_loop)
                self.thread.start()

    def stop_playback(self):
        with self.lock:
            if self.playing:
                self.playing = False
        if self.thread:
            self.thread.join()
        self.outport.reset()

    def save_and_restart(self, new_midi_filename):
        self.stop_playback()
        self.midi_filename = new_midi_filename
        self.start_playback()

    def __del__(self):
        try:
            self.stop_playback()
            if self.outport and self.outport.is_open:
                self.outport.close()
        except Exception as e:
            print(f"Error during cleanup: {e}")

if __name__ == "__main__":
    player = CPlayback('output.mid')
    player.start_playback()
    time.sleep(10)  # Let it play for 10 seconds
    player.save_and_restart('output.mid')
