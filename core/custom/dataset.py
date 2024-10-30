import os
import torch
from torch.utils.data import Dataset
from music21 import converter, instrument, note, chord

class MIDIDataset(Dataset):
    def __init__(self, midi_dir, seq_length):
        """
        Args:
            midi_dir (str): Path to the directory containing MIDI files.
            seq_length (int): Sequence length for training the model.
        """
        self.midi_dir = midi_dir
        self.seq_length = seq_length
        self.midi_files = [os.path.join(midi_dir, f) for f in os.listdir(midi_dir) if f.endswith('.mid')]

        # Store parsed note sequences
        self.notes = self._parse_midi_files()

        # Create mapping from notes/chords to integers
        self.note_to_int = {n: i for i, n in enumerate(sorted(set(self.notes)))}
        self.int_to_note = {i: n for n, i in self.note_to_int.items()}

        # Tokenize the notes
        self.tokenized_notes = [self.note_to_int[n] for n in self.notes]

    def _parse_midi_files(self):
        """Parse all MIDI files in the directory and extract notes and chords."""
        all_notes = []
        for midi_file in self.midi_files:
            midi = converter.parse(midi_file)

            parts = instrument.partitionByInstrument(midi)
            notes = []

            if parts:  # File has instrument parts
                for part in parts.parts:
                    notes_to_parse = part.recurse()
                    for element in notes_to_parse:
                        if isinstance(element, note.Note):
                            notes.append(str(element.pitch))
                        elif isinstance(element, chord.Chord):
                            notes.append('.'.join(str(n) for n in element.normalOrder))
            else:  # No parts, assume it's a flat structure
                notes_to_parse = midi.flat.notes
                for element in notes_to_parse:
                    if isinstance(element, note.Note):
                        notes.append(str(element.pitch))
                    elif isinstance(element, chord.Chord):
                        notes.append('.'.join(str(n) for n in element.normalOrder))

            all_notes.extend(notes)

        return all_notes

    def __len__(self):
        """Return the number of training sequences available."""
        return len(self.tokenized_notes) - self.seq_length

    def __getitem__(self, index):
        """Generate one training sequence."""
        seq_in = self.tokenized_notes[index:index+self.seq_length]
        seq_out = self.tokenized_notes[index+1:index+self.seq_length+1]
        return torch.tensor(seq_in, dtype=torch.long), torch.tensor(seq_out, dtype=torch.long)