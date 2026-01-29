import unittest
import warnings
from unittest.mock import patch, MagicMock
from urllib.error import URLError

from etlsus.extraction import extract


class TestExtract(unittest.TestCase):

    @patch('etlsus.extraction.extraction.Path')
    @patch('etlsus.extraction.extraction.config.RAW_DIR', '/mock/raw/dir')
    @patch('etlsus.extraction.extraction.urlretrieve')
    def test_extract_successful_downloads(
            self, mock_urlretrieve, mock_path
    ):
        mock_output_path = MagicMock()
        mock_output_path.exists.return_value = False

        mock_path_instance = MagicMock()
        mock_path.return_value = mock_path_instance
        mock_path_instance.__truediv__.return_value = mock_output_path

        cfg = {
            'files': {
                '2020': 'https://example.com/data2020.csv',
                '2021': 'https://example.com/data2021.csv'
            },
            'prefix': 'prefix_'
        }

        extract(cfg)

        self.assertEqual(mock_urlretrieve.call_count, 2)

    @patch('etlsus.extraction.extraction.Path')
    @patch('etlsus.extraction.extraction.config.RAW_DIR', '/mock/raw/dir')
    @patch('etlsus.extraction.extraction.urlretrieve')
    def test_extract_years_to_extract(
            self, mock_urlretrieve, mock_path
    ):
        mock_output_path = MagicMock()
        mock_output_path.exists.return_value = False

        mock_path_instance = MagicMock()
        mock_path.return_value = mock_path_instance
        mock_path_instance.__truediv__.return_value = mock_output_path

        cfg = {
            'files': {
                '2020': 'https://example.com/data2020.csv',
                '2021': 'https://example.com/data2021.csv'
            },
            'prefix': 'prefix_'
        }

        extract(cfg, years_to_extract=['2021'])

        self.assertEqual(mock_urlretrieve.call_count, 1)

    @patch('etlsus.extraction.extraction.Path')
    @patch('etlsus.extraction.extraction.config.RAW_DIR', '/mock/raw/dir')
    @patch('etlsus.extraction.extraction.urlretrieve')
    def test_extract_skips_existing_files(self, mock_url, mock_path):
        mock_output_path = MagicMock()
        mock_output_path.exists.return_value = True

        mock_path_instance = MagicMock()
        mock_path.return_value = mock_path_instance
        mock_path_instance.__truediv__.return_value = mock_output_path

        cfg = {
            'files': {'1': 'https://downloaded_file.csv'},
            'prefix': 'prefix_'
        }

        extract(cfg)

        mock_url.assert_not_called()

    @patch('etlsus.extraction.extraction.Path')
    @patch('etlsus.extraction.extraction.config.RAW_DIR', '/mock/raw/dir')
    @patch('etlsus.extraction.extraction.urlretrieve')
    def test_extract_handles_download_errors(
            self, mock_urlretrieve, mock_path
    ):
        mock_output_path = MagicMock()
        mock_output_path.exists.return_value = False

        mock_path_instance = MagicMock()
        mock_path.return_value = mock_path_instance
        mock_path_instance.__truediv__.return_value = mock_output_path

        cfg = {
            'files': {'1': 'https://example.com/badurl.csv'},
            'prefix': 'prefix_'
        }

        mock_urlretrieve.side_effect = URLError

        with warnings.catch_warnings(record=True) as w:
            extract(cfg)

            self.assertEqual(len(w), 1)
            self.assertIn(
                'Failed to download', str(w[0].message)
            )

    @patch('etlsus.extraction.extraction.config')
    def test_extract_empty_dataset(self, mock_config):
        mock_config.RAW_DIR = '/mock/raw/dir'

        dataset = {
            'files': {},
            'prefix': 'foo'
        }

        extract(dataset)


if __name__ == '__main__':
    unittest.main()
