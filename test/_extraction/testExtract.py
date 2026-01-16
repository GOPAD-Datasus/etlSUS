import os
import unittest
import warnings
from unittest.mock import patch
from urllib.error import URLError

from etlsus import extract


class TestExtract(unittest.TestCase):

    @patch('etlsus.extraction.extraction.config.RAW_DIR', '/mock/raw/dir')
    @patch('etlsus.extraction.extraction.get_yaml_urls')
    @patch('etlsus.extraction.extraction.file_exists')
    @patch('etlsus.extraction.extraction.urlretrieve')
    def test_extract_successful_downloads(self,
                                          mock_urlretrieve,
                                          mock_file_exists,
                                          mock_get_yaml):
        mock_get_yaml.return_value = (
            {'2020': 'http://example.com/data2020.csv',
             '2021': 'http://example.com/data2021.csv'},
            'prefix_'
        )

        mock_file_exists.return_value = False

        extract('dummy_input.yaml')

        mock_get_yaml.assert_called_once_with('dummy_input.yaml')
        self.assertEqual(mock_file_exists.call_count, 2)
        self.assertEqual(mock_urlretrieve.call_count, 2)

        expected_path1 = os.path.join('/mock/raw/dir', 'prefix_2020.csv')
        expected_path2 = os.path.join('/mock/raw/dir', 'prefix_2021.csv')

        mock_urlretrieve.assert_any_call('http://example.com/data2020.csv',
                                         expected_path1)
        mock_urlretrieve.assert_any_call('http://example.com/data2021.csv',
                                         expected_path2)

    @patch('etlsus.extraction.extraction.config.RAW_DIR', '/mock/raw/dir')
    @patch('etlsus.extraction.extraction.get_yaml_urls')
    @patch('etlsus.extraction.extraction.file_exists')
    @patch('etlsus.extraction.extraction.urlretrieve')
    def test_extract_skips_existing_files(self,
                                          mock_urlretrieve,
                                          mock_file_exists,
                                          mock_get_yaml):
        mock_get_yaml.return_value = (
            {'2020': 'http://example.com/data2020.csv',
             '2021': 'http://example.com/data2021.csv'},
            'prefix_'
        )

        def mock_check_side_effect(path):
            return '2020' in path

        mock_file_exists.side_effect = mock_check_side_effect

        extract('dummy_input.yaml')

        mock_urlretrieve.assert_called_once_with(
            'http://example.com/data2021.csv',
            os.path.join('/mock/raw/dir', 'prefix_2021.csv')
        )

    @patch('etlsus.extraction.extraction.config.RAW_DIR', '/mock/raw/dir')
    @patch('etlsus.extraction.extraction.get_yaml_urls')
    @patch('etlsus.extraction.extraction.file_exists')
    @patch('etlsus.extraction.extraction.urlretrieve')
    def test_extract_handles_download_errors(self,
                                             mock_urlretrieve,
                                             mock_file_exists,
                                             mock_get_yaml):
        mock_get_yaml.return_value = (
            {'2020': 'http://example.com/data2020.csv',
             '2021': 'http://example.com/badurl.csv'},
            'prefix_'
        )

        mock_file_exists.return_value = False

        def mock_urlretrieve_side_effect(url, filename):
            if 'badurl' in url:
                raise URLError('404 Not Found')
            return None

        mock_urlretrieve.side_effect = mock_urlretrieve_side_effect

        with warnings.catch_warnings(record=True) as w:
            extract('dummy_input.yaml')

            mock_urlretrieve.assert_any_call(
                'http://example.com/data2020.csv',
                os.path.join('/mock/raw/dir', 'prefix_2020.csv')
            )

            self.assertEqual(len(w), 1)
            self.assertIn('Failed to download 2021',
                          str(w[0].message))

    @patch('etlsus.extraction.extraction.config.RAW_DIR', '/mock/raw/dir')
    @patch('etlsus.extraction.extraction.get_yaml_urls')
    def test_extract_empty_yaml(self, mock_get_yaml):
        mock_get_yaml.return_value = ({}, 'prefix_')

        extract('dummy_input.yaml')


if __name__ == '__main__':
    unittest.main()
