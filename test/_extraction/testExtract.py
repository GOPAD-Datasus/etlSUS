import unittest
import warnings
from pathlib import Path
from unittest.mock import patch
from urllib.error import URLError

from etlsus import extract


class TestExtract(unittest.TestCase):

    @patch('etlsus.extraction.extraction..config.RAW_DIR', '/mock/raw/dir')
    @patch('etlsus.extraction.extraction.file_exists')
    @patch('etlsus.extraction.extraction.urlretrieve')
    def test_extract_successful_downloads(self,
                                          mock_urlretrieve,
                                          mock_file_exists):
        dataset = {
            'files': {
                '2020': 'https://example.com/data2020.csv',
                '2021': 'https://example.com/data2021.csv'
            },
            'prefix': 'prefix_'
        }

        mock_file_exists.return_value = False

        extract(dataset)

        self.assertEqual(mock_file_exists.call_count, 2)
        self.assertEqual(mock_urlretrieve.call_count, 2)

        expected_path1 = Path('/mock/raw/dir', 'prefix_2020.csv')
        expected_path2 = Path('/mock/raw/dir', 'prefix_2021.csv')

        mock_urlretrieve.assert_any_call(
            'https://example.com/data2020.csv', expected_path1
        )
        mock_urlretrieve.assert_any_call(
            'https://example.com/data2021.csv', expected_path2
        )

    @patch('etlsus.extraction.extraction..config.RAW_DIR', '/mock/raw/dir')
    @patch('etlsus.extraction.extraction.file_exists')
    def test_extract_skips_existing_files(self, mock_file_exists):
        dataset = {
            'files': {'1': 'https://downloaded_file.csv'},
            'prefix': 'prefix_'
        }

        def mock_check_side_effect(path):
            return path.name == 'downloaded_file.csv'

        mock_file_exists.side_effect = mock_check_side_effect

        extract(dataset)

    @patch('etlsus.extraction.extraction..config.RAW_DIR', '/mock/raw/dir')
    @patch('etlsus.extraction.extraction.file_exists')
    @patch('etlsus.extraction.extraction.urlretrieve')
    def test_extract_handles_download_errors(self,
                                             mock_urlretrieve,
                                             mock_file_exists):
        dataset = {
            'files': {'1': 'https://example.com/badurl.csv'},
            'prefix': 'prefix_'
        }

        mock_file_exists.return_value = False

        def mock_urlretrieve_side_effect(url, filename):
            if 'badurl' in url:
                raise URLError('404 Not Found')
            return None

        mock_urlretrieve.side_effect = mock_urlretrieve_side_effect

        with warnings.catch_warnings(record=True) as w:
            extract(dataset)

            self.assertEqual(len(w), 1)
            self.assertIn('Failed to download',
                          str(w[0].message))

    @patch('etlsus.extraction.extraction..config.RAW_DIR', '/mock/raw/dir')
    def test_extract_empty_dataset(self):
        dataset = {
            'files': {},
            'prefix': 'foo'
        }

        extract(dataset)


if __name__ == '__main__':
    unittest.main()
