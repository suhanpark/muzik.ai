import unittest
from unittest.mock import patch, MagicMock
from ..utils.gather_data import gather_audio_data
from ..utils.gcs import GCS

class TestGatherData(unittest.TestCase):

    @patch('utils.gather_data.get_video_links', return_value=['video_link_1', 'video_link_2'])
    @patch('tqdm.tqdm')
    @patch('utils.gather_data.GCS')
    def test_gather_audio_data(self, mock_gcs, mock_tqdm, mock_get_video_links):
        # Mock GCS object methods
        mock_gcs_instance = mock_gcs.return_value
        mock_gcs_instance.upload_audio_files = MagicMock()
        mock_gcs_instance.blob_count_refresh = MagicMock()
        mock_gcs_instance.wav_blob_count = 5
        mock_gcs_instance.midi_blob_count = 3

        result = gather_audio_data(mock_gcs_instance)
        self.assertEqual(result, "Uploading Audio Files Complete.\nTotal WAV Files: 5\nTotal MIDI Files: 3")

        mock_get_video_links.assert_called_once()
        mock_gcs_instance.upload_audio_files.assert_called()
        mock_gcs_instance.blob_count_refresh.assert_called()

if __name__ == '__main__':
    unittest.main()
