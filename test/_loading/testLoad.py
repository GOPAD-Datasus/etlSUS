import unittest
import warnings
from unittest.mock import patch, MagicMock

from etlsus.loading import load


class TestLoad(unittest.TestCase):
    module = 'etlsus.loading.loading'

    @patch(f'{module}.pd.read_parquet')
    @patch(
        f'{module}.get_files_from_dir',
        return_value=["file1.parquet", "file2.parquet"]
    )
    @patch(f'{module}.config.PROCESSED_DIR', '/processed')
    def test_load_success(
            self, mock_get_files, mock_read_parquet
    ):
        mock_df = MagicMock()
        mock_engine = MagicMock()

        mock_read_parquet.return_value = mock_df

        load(
            database_engine=mock_engine,
            table_name='test_table'
        )

        mock_get_files.assert_called_with(
            '/processed', extension='.parquet.gzip', infix=None
        )

        self.assertEqual(mock_read_parquet.call_count, 2)
        self.assertEqual(mock_df.to_sql.call_count, 2)
        mock_engine.connect.assert_called_once()

    @patch(f'{module}.pd.read_parquet')
    @patch(f'{module}.get_files_from_dir')
    def test_load_no_file(self, mock_get_files, mock_read_parquet):
        mock_engine = MagicMock()
        mock_get_files.return_value = []

        load(mock_engine, 'table_test')

        mock_read_parquet.assert_not_called()

    @patch(f'{module}.pd.read_parquet')
    @patch(f'{module}.get_files_from_dir')
    def test_load_database_failure(self, mock_get_files, mock_read_parquet):
        mock_engine = MagicMock()

        mock_get_files.return_value = ['file1.parquet']

        mock_df = MagicMock()
        mock_df.to_sql.side_effect = Exception('Failed to find insert')
        mock_read_parquet.return_value = mock_df

        with warnings.catch_warnings(record=True) as w:
            load(mock_engine, 'test_table')
            self.assertEqual(len(w), 1)
            self.assertIn('Failed to load', str(w[0].message))


if __name__ == '__main__':
    unittest.main()
