import unittest
from unittest.mock import patch, MagicMock

from etlsus.transformation import transform


class TestTransformation(unittest.TestCase):
    module = 'etlsus.transformation.transformation'

    @patch(f'{module}.config')
    @patch(
        f'{module}.get_files_from_dir', return_value=['raw.csv', 'raw2.csv']
    )
    @patch(f'{module}.get_file_name', return_value='raw')
    @patch(f'{module}.FileProcessor', return_value=MagicMock())
    def test_transform_success(
            self,
            mock_file_processor,
            mock_get_file_name,
            mock_get_files,
            mock_config,
    ):
        mock_config.RAW_DIR = '/mock/raw/dir'
        mock_config.PROCESSED_DIR = MagicMock()

        mock_proc_file = MagicMock()
        mock_proc_file.exists.return_value = False
        mock_config.PROCESSED_DIR.__truediv__.return_value = mock_proc_file

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

    @patch(f'{module}.config')
    @patch(f'{module}.get_files_from_dir')
    def test_transform_no_files(self, mock_get_files, mock_config):
        mock_config.RAW_DIR = '/mock/raw/dir'
        mock_get_files.return_value = []

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
