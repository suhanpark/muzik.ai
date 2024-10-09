import unittest
from unittest.mock import patch, MagicMock
from ..utils.file_converter import mp42wav, wav2mid

sample_dir = 'data/sample'

class TestFileConverter(unittest.TestCase):

    @patch('subprocess.run')
    def test_mp42wav_success(self, mock_run):
        # Mock the subprocess.run to simulate successful conversion
        mock_run.return_value = MagicMock()
        result = mp42wav('sample.mp4', 'output.wav')
        self.assertIsNone(result)
        mock_run.assert_called_once_with(['ffmpeg', '-i', 'sample.mp4', '-q:a', '0', '-map', 'a', 'output.wav'], check=True)

    @patch('subprocess.run', side_effect=Exception('Conversion failed'))
    def test_mp42wav_failure(self, mock_run):
        result = mp42wav('sample.mp4', 'output.wav')
        self.assertIsNone(result)
        mock_run.assert_called_once()

    @patch('subprocess.run')
    def test_wav2mid_success(self, mock_run):
        # Mock the subprocess.run to simulate successful conversion
        mock_run.return_value = MagicMock()
        result = wav2mid('sample.wav', 'output.mid')
        self.assertIsNone(result)
        mock_run.assert_called_once_with(['waon', '-i', 'sample.wav', '-o', 'output.mid'], check=True)

    @patch('subprocess.run', side_effect=Exception('Conversion failed'))
    def test_wav2mid_failure(self, mock_run):
        result = wav2mid('sample.wav', 'output.mid')
        self.assertIsNone(result)
        mock_run.assert_called_once()

if __name__ == '__main__':
    unittest.main()
