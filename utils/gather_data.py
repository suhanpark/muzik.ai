from gcs import GCS
from scraper import get_video_links
from tqdm import tqdm

def gather_audio_data(db: GCS) -> str:
    """
    Complete function to download YouTube videos, convert files (MP4 -> WAV, WAV -> MIDI),
    and upload them to corresponding GCS buckets.

    :param GCS db: database object (GCS), defaulted to gcs
    :return str: work complete message
    """
    
    db.blob_count_refresh()
    
    video_links = get_video_links(num_videos=30)
    print(f"\nTotal Video Links: {len(video_links)}\n")
    
    for link in tqdm(video_links, desc='Uploading files to GCS'):
        db.upload_audio_files(link)
    
    db.blob_count_refresh()
    return f"Uploading Audio Files Complete.\nTotal WAV Files: {db.wav_blob_count}\nTotal MIDI Files: {db.midi_blob_count}"

if __name__ == '__main__':
    gcs = GCS()
    print(gather_audio_data(db=gcs))