import subprocess
import essentia.standard as es
import numpy as np
from mido import MidiFile, MidiTrack, Message

def mp42wav(mp4_file: str, output_audio_file: str):
    """
    Run FFmpeg command to extract audio from MP4 file

    :param _type_ mp4_file: _description_
    :param _type_ output_audio_file: _description_
    """
    
    try:
        command = ['ffmpeg', '-i', mp4_file, '-q:a', '0', '-map', 'a', output_audio_file]
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"Error during mp4 to wav conversion: {e}")
        return

def wav2mid(wav_path: str, midi_path: str) -> None:
    """
    Convert wav to mid

    :param str wav_path: wav file path
    :param str midi_path: mid file path
    """
    
    try:
        pitch_values = extract_melody_from_wav(wav_path)
        convert_to_midi(pitch_values, midi_path)
    except Exception as e:
        print(f"Error during WAV to MIDI conversion: {e}")
        return

def extract_melody_from_wav(wav_file):
    """
    extract pitch values from wav file

    :param _type_ wav_file: wav file
    :return _type_: pitch values
    """
    
    # Load the audio file
    loader = es.MonoLoader(filename=wav_file)
    audio = loader()

    # Extract the melody using the Melodia algorithm
    pitch_extractor = es.PitchMelodia()
    pitch_values, _ = pitch_extractor(audio)

    return pitch_values

def hz_to_midi(pitch_hz):
    """
    Convert frequency (Hz) to a valid MIDI note number.

    :param _type_ pitch_hz: pitch hz value from wav file
    :return _type_: None
    """
    
    if pitch_hz > 0:  # Only process voiced frames (pitch > 0)
        midi_note = 69 + 12 * np.log2(pitch_hz / 440.0)
        return int(round(midi_note))
    
    # Return None for unvoiced frames (silence)
    return None  

def convert_to_midi(pitch_values, output_midi_file):
    """
    takes tracks from wav

    :param _type_ pitch_values: pitch values from wav
    :param _type_ output_midi_file: .mid file
    """
    
    # Create a new MIDI file
    midi = MidiFile()
    track = MidiTrack()
    midi.tracks.append(track)

    # Convert pitch values to MIDI notes
    for pitch in pitch_values:
        if pitch > 0:  # Only consider voiced frames
            note = hz_to_midi(pitch)
            msg = Message('note_on', note=note, velocity=64)
            track.append(msg)

    # Save the MIDI file
    try:
        print(output_midi_file)
        midi.save(output_midi_file)
    except Exception as e:
        print(f"Error during MIDI conversion: {e}")
        return

