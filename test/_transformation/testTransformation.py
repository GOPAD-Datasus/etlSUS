import unittest
from unittest.mock import patch

from etlsus import transform


class TestTransformation(unittest.TestCase):
    module = 'etlsus.transformation.transformation'

    @patch(f'{module}.config.RAW_DIR', '/mock/raw/dir')
    @patch(f'{module}.get_files_from_dir',
           return_value=['raw.csv', 'raw2.csv'])
    @patch(f'{module}.check_if_processed', return_value=False)
    @patch(f'{module}.transform_file')
    def test_transform_success(self, mock_transform_file,
                               mock_check, mock_get_files):

        transform()

        self.assertEqual(2, mock_transform_file.call_count)
        mock_transform_file.assert_called_with('raw2.csv', None)

    @patch(f'{module}.config.RAW_DIR', '/mock/raw/dir')
    @patch(f'{module}.get_files_from_dir',
           return_value=[])
    @patch(f'{module}.check_if_processed', return_value=False)
    @patch(f'{module}.transform_file')
    def test_transform_no_files(self, mock_transform_file,
                                mock_check, mock_get_files):
        transform()

        self.assertEqual(0, mock_transform_file.call_count)
