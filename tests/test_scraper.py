import unittest
from unittest.mock import patch
from utils.gather_data import get_video_links 

class TestScraper(unittest.TestCase):

    @patch('utils.scraper.VideosSearch')
    def test_get_video_links(self, mock_videos_search):
        mock_instance = mock_videos_search.return_value
        mock_instance.result.return_value = {
            'result': [
                {'id': 'video1', 'isLive': False, 'channel': 'NotSUPARQ', 'duration': '01:15'},
                {'id': 'video2', 'isLive': False, 'channel': 'SUPARQ', 'duration': '01:15'},
                {'id': 'video3', 'isLive': True, 'channel': 'NotSUPARQ', 'duration': '01:15'},
                {'id': 'video4', 'isLive': True, 'channel': 'NotSUPARQ', 'duration': '01:00'}
            ]
        }
        mock_instance.next.return_value = None

        result = get_video_links(num_videos=2)
        self.assertEqual(result, ['https://www.youtube.com/watch?v=video1',
                                  'https://www.youtube.com/watch?v=video4'])
        mock_videos_search.assert_called_once_with('lofi hip hop', limit=15)

if __name__ == '__main__':
    unittest.main()
