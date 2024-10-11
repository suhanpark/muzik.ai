from google.cloud import storage
from google.cloud.storage.bucket import Bucket 
from pytubefix import YouTube
from file_converter import mp42wav, wav2mid
import os

class GCS(object):
    """
    Custom GCS Object for efficient structure
    """
    
    def __init__(self):
        """
        Initializes GCS object.
        """
        
        self.storage_client = storage.Client()
        self.wav_bucket = self.storage_client.bucket('muzik_wav')
        self.midi_bucket = self.storage_client.bucket('muzik_midi')

        self.wav_blob_count = self.get_blob_count(self.wav_bucket)
        self.midi_blob_count = self.get_blob_count(self.midi_bucket)
    
    def blob_count_refresh(self) -> None:
        """
        refeshes blob counts for buckets
        """
        
        self.wav_blob_count = self.get_blob_count(self.wav_bucket)
        self.midi_blob_count = self.get_blob_count(self.midi_bucket)
        
        print(f"WAV Blob Count Refreshed: {self.wav_blob_count}")
        print(f"MIDI Blob Count Refreshed: {self.midi_blob_count}\n")
    
    def get_blob_count(self, bucket: Bucket, prefix: str = None) -> int:
        """
        Counts the number of files (objects) in a Google Cloud Storage bucket.

        :param Bucket bucket_name: The name of the GCS bucket.
        :param str prefix: The prefix (folder path) to count files in, defaults to None
        :return int: The number of files in the bucket or within the specified folder.
        """

        # List all objects in the bucket or folder (prefix)
        blobs = bucket.list_blobs(prefix=prefix)

        # Count the number of files (blobs)
        file_count = len(list(blobs))
        return file_count

    def to_bucket(self, bucket: Bucket, source_file_path: str, destination_blob_name: str) -> None:
        """
        Uploads a .wav file to the Google Cloud Storage bucket.

        :param Bucket bucket: The GCS bucket object.
        :param str source_file_path: The local path to the .wav file to upload.
        :param str destination_blob_name: The name of the file in GCS.
        """
        
        # Create a blob object in the bucket with the destination name
        blob = bucket.blob(destination_blob_name)

        # Upload the file to GCS
        blob.upload_from_filename(source_file_path)
        
    def upload_audio_files(self, video_url: str, output_path : str = 'data') -> None:
        """
        downloading videos to the specified folder then uploads to GCS
        YouTube (.mp4) -> wav_bucket (.wav) -> midi_bucket (.mid)

        :param str video_url: video url to download
        :param str output_path: temporary directory to hold .wav files, defaults to 'data'
        """
        
        title = f'{self.wav_blob_count}'.zfill(3)
        yt = YouTube(video_url)

        # Filter streams to only get audio, and select the best quality audio
        video_stream = yt.streams.filter(only_audio=True).first()

        # Download the video file (.mp4)
        wav_folder = os.path.join(output_path, 'wav_audio')
        os.makedirs(wav_folder, exist_ok=True)

        downloaded_file = video_stream.download(wav_folder)

        wav_filename = f"{title}.wav"
        final_wav_file = os.path.join(wav_folder, wav_filename)
        mp42wav(downloaded_file, final_wav_file)
        
        midi_folder = os.path.join(output_path, 'midi_audio')
        os.makedirs(midi_folder, exist_ok=True)

        midi_filename = f"{title}.mid"
        final_midi_file = os.path.join(midi_folder, midi_filename)
        wav2mid(final_wav_file, final_midi_file)
        
        self.to_bucket(self.wav_bucket, final_wav_file, wav_filename)
        self.wav_blob_count += 1
        
        self.to_bucket(self.midi_bucket, final_midi_file, midi_filename)
        self.midi_blob_count += 1
        
        # remove converted file to save storage
        os.remove(downloaded_file)
        os.remove(final_wav_file)
        os.remove(final_midi_file)
        
        return
        