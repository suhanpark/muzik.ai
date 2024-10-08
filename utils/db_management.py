from gcs import GCS
from scraper import get_video_links
from tqdm import tqdm


def gather_audio_data(db: GCS) -> str:
    """
    Complete function to download YouTube videos, convert files (MP4 -> WAV, WAV -> MIDI),
    and upload them to corresponding GCS buckets.

    :param GCS db: database object (GCS)
    :return str: work complete message
    """
    db.blob_count_refresh()
    
    video_links = get_video_links()
    
    for link in tqdm(video_links, desc='Uploading files to GCS'):
        db.upload_audio_files(link)
    
    db.blob_count_refresh()
    return f"Uploading Audio Files Complete.\nTotal WAV Files: {db.wav_blob_count}\nTotal MIDI Files: {db.midi_blob_count}"
