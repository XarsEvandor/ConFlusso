from mido import MidiFile


def inspect_midi(filename):
    midi = MidiFile(filename)

    for i, track in enumerate(midi.tracks):
        print(f"Track {i}: {track.name}")
        for msg in track:
            print(msg)


if __name__ == "__main__":
    filename = 'output.mid'  # Replace with your MIDI file's name if different
    inspect_midi(filename)
