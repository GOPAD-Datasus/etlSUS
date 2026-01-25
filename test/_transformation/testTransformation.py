import unittest
from unittest.mock import patch, MagicMock

from etlsus import transform


class TestTransformation(unittest.TestCase):
    module = 'etlsus.transformation.transformation'

    @patch(f'{module}.RAW_DIR', '/mock/raw/dir')
    @patch(
        f'{module}.get_files_from_dir', return_value=['raw.csv', 'raw2.csv']
    )
    @patch(f'{module}.get_file_name', return_value='raw')
    @patch(f'{module}.file_exists', return_value=False)
    @patch(f'{module}.FileProcessor', return_value=MagicMock())
    def test_transform_success(
            self,
            mock_file_processor,
            mock_file_exists,
            mock_get_file_name,
            mock_get_files
    ):
        cfg = MagicMock()
        cfg.get.return_value = 'DN'

        transform(
            cfg,
            True,
            True,
            True,
            True,
            True
        )

        self.assertEqual(2, mock_file_processor.call_count)

    @patch(f'{module}.RAW_DIR', '/mock/raw/dir')
    @patch(f'{module}.get_files_from_dir', return_value=[])
    def test_transform_no_files(self, mock_get_files):
        cfg = MagicMock()
        cfg.get.return_value = 'DN'

        transform(
            cfg,
            True,
            True,
            True,
            True,
            True
        )


if __name__ == '__main__':
    unittest.main()
