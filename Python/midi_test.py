from mido import MidiFile, open_output, bpm2tempo, tick2second
import time

def inspect_and_play_midi(filename):
    # Load the MIDI file
    midi = MidiFile(filename)
    tpb = midi.ticks_per_beat  # Ticks per beat
    current_tempo = bpm2tempo(120)  # Default MIDI tempo (120 BPM)

    # Inspect MIDI file
    for i, track in enumerate(midi.tracks):
        print(f"Track {i}: {track.name}")
        for msg in track:
            print(msg)

    # Play the MIDI file
    with open_output() as outport:
        for msg in midi.play():
            if not msg.is_meta:
                outport.send(msg)
            if msg.time > 0:
                sleep_time = tick2second(msg.time, tpb, current_tempo)
                time.sleep(sleep_time)
            if msg.type == 'set_tempo':
                current_tempo = msg.tempo  # Update the tempo
            if msg.type == 'end_of_track':  # Handle end of track
                break

if __name__ == "__main__":
    filename = 'samples\Allegro-Music-Transformer-MI-Seed-2.mid'  # Replace with your MIDI file's name if different
    inspect_and_play_midi(filename)
    exit(0)
