import subprocess

def mp42wav(mp4_file: str, output_audio_file: str):
    """
    Run FFmpeg command to extract audio from MP4 file

    :param _type_ mp4_file: _description_
    :param _type_ output_audio_file: _description_
    """
    try:
        command = ['ffmpeg', '-i', mp4_file, '-q:a', '0', '-map', 'a', output_audio_file]
        subprocess.run(command, check=True)
    except Exception as e:
        print(f"Error during mp4 to wav conversion: {e}")
        return

def wav2mid(wav_path: str, midi_path: str) -> None:
    try:
        command = ['waon', '-i', wav_path, '-o', midi_path]
        subprocess.run(command, check=True)
    except Exception as e:
        print(f"Error during WAV to MIDI conversion: {e}")
        return

