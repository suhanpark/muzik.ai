from typing import List
from youtubesearchpython import VideosSearch

def get_video_links(genre: str = 'lofi hip hop', num_videos: int = 100) -> List[str]:
    """
    Get a list of YouTube video links for lofi hip-hop that are not live.

    :return _type_: _description_
    """
    
    video_links = []
    videos_search = VideosSearch(genre, limit=15)  # Fetch 15 results per page

    while len(video_links) < num_videos:
        results = videos_search.result()['result']

        for video in results:
            channel = video.get('channel')
            
            # Exclude live videos and videos from my channel
            if not video.get('isLive') and channel != 'SUPARQ':  
              duration = video.get('duration')
              if duration:
                hour = int(duration.split(':')[0])
                minute = int(duration.split(':')[1])

                if hour == 1 and minute <= 30:
                  video_links.append(f"https://www.youtube.com/watch?v={video['id']}")

                  if len(video_links) >= num_videos:
                      break

        # Fetch the next page of results if needed
        if len(video_links) < num_videos:
            # Move to the next page of search results
            videos_search.next() 

    return video_links