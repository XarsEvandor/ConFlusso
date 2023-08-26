import rtmidi
import threading
import time

class CMidi_old:
    def __init__(self):
        self.midiout = rtmidi.MidiOut()
        available_ports = self.midiout.get_ports()
        if available_ports:
            self.midiout.open_port(0)
        else:
            print("No MIDI port found")

        self.is_playing = False
        self.set_duration = True
        self.lock = threading.Lock()

        self.running = True
        self.thread = threading.Thread(target=self._run)
        self.thread.start()

    def _run(self):
        while self.running:
            with self.lock:
                if self.is_playing and self.set_duration:
                    notes, velocity, duration, channel = self.note_data
                    
                    # Check if the channel is valid
                    if channel not in range(16): 
                        channel = 0
                    
                    for note in notes:
                        self.send_note_on(note, velocity, channel)
                        time.sleep(duration)
                        self.send_note_off(note, channel)
                    self.is_playing = False  # Note has finished playing
                else:
                    time.sleep(0.01)  # No tight loops, sleep for a brief moment

    def play_note(self, notes, velocity=100, duration=0.5, set_duration=True, channel = 0):
        with self.lock:
            if not self.is_playing:
                self.is_playing = True
                self.set_duration = set_duration
                
                # Check if the channel is valid
                if channel not in range(16): 
                    channel = 0
                    
                self.note_data = (notes, velocity, duration, channel)
                if not set_duration:  # If the note is to be sustained indefinitely
                    for note in notes:
                        self.send_note_on(note, velocity, channel)

    def stop_note(self, note, channel):
        with self.lock:
            if self.is_playing and not self.set_duration:
                notes, _, _, channel = self.note_data
                for note in notes:
                    self.send_note_off(note, channel)
                self.is_playing = False  # Reset the state

    def send_note_on(self, note, velocity, channel = 0):
        note_on = [0x90 + channel, note, velocity]
        self.midiout.send_message(note_on)

    def send_note_off(self, note, channel = 0):
        note_off = [0x80 + channel, note, 0]
        self.midiout.send_message(note_off)
        
    def change_instrument(self, instrument, channel=0):
        """
        Change the instrument on a given channel.
        :param instrument: Instrument number (0-127)
        :param channel: MIDI channel (0-15)
        """
        if 0 <= instrument <= 127 and 0 <= channel <= 15:
            program_change = [0xC0 + channel, instrument]
            self.midiout.send_message(program_change)
        else:
            print("Invalid instrument or channel number")

    def close(self):
        self.running = False
        self.thread.join()
        self.midiout.close_port()

if __name__ == "__main__":
    mm = CMidi_old()
    
    mm.play_note([60], 112, set_duration=True)  # Play middle C for a specific duration
    time.sleep(1)
    mm.play_note([69,72,65], 112, set_duration=False)  # Sustain chord indefinitely
    time.sleep(3)
    mm.stop_note()  # Stop the indefinitely sustained note
    mm.play_note([60], 112, 2, set_duration=True)  # Play middle C for the default duration
    time.sleep(2.2)
    
    # Set instruments
    mm.change_instrument(40, channel=1)  # Violin
    mm.change_instrument(0, channel=2)   # Piano
    mm.change_instrument(42, channel=3)  # Cello
    mm.change_instrument(24, channel=4)  # Guitar

    end_time = time.time() + 10  # Play for 10 seconds

    while time.time() < end_time:
        # Instruments play their respective notes concurrently for 0.5 seconds

        # Piano plays a C Major chord
        piano_notes = [60, 64, 67]
        mm.play_note(piano_notes, 100, set_duration=False, channel=2)
        
        # Violin plays High C
        violin_note = [72]
        mm.play_note(violin_note, 90, set_duration=False, channel=1)
        
        # Cello plays Low C
        cello_note = [48]
        mm.play_note(cello_note, 80, set_duration=False, channel=3)
        
        # Guitar strums a C Major chord
        guitar_notes = [60, 63, 67]
        mm.play_note(guitar_notes, 90, set_duration=False, channel=4)

        time.sleep(0.5)

        # Stop notes for each instrument after they've played concurrently for 0.5 seconds
        for note in piano_notes:
            mm.stop_note(note, 2)
        mm.stop_note(violin_note[0], 1)
        mm.stop_note(cello_note[0], 3)
        for note in guitar_notes:
            mm.stop_note(note, 4)

        time.sleep(0.5)  # Pause for 0.5 seconds before repeating

    # Stop all notes
    mm.stop_note()

    mm.close()  # Close the MIDI connection



