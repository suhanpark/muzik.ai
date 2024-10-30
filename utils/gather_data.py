from utils.gcs import GCS
from scraper import get_video_links
from tqdm import tqdm
import os
import pickle

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
    if os.path.exists('utils/gcs.pkl'):
        with open('utils/gcs.pkl', 'rb') as file:
            gcs = pickle.load(file)
    else:
        gcs = GCS()
        
        with open('utils/gcs.pkl', 'wb') as file:
            pickle.dump(gcs, file)
        
    if gcs.midi_blob_count > 0:
        print(gcs.download_midi())
    else:
        print(gather_audio_data(db=gcs))
    
    with open('utils/gcs.pkl', 'wb') as file:
            pickle.dump(gcs, file)