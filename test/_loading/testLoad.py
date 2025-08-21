import unittest
import warnings
from unittest.mock import patch, MagicMock

from etlsus import load


class TestLoad(unittest.TestCase):
    module = 'etlsus.loading.loading'

    @patch(f'{module}.insert_into_db')
    @patch(f'{module}.pd.read_parquet', return_value=MagicMock())
    @patch(f'{module}.get_files_from_dir',
           return_value=["file1.parquet", "file2.parquet"])
    @patch(f'{module}.create_db_engine')
    @patch(f'{module}.config.PROCESSED_DIR', '/processed')
    def test_load_success(self, mock_create_engine, mock_get_files,
                          mock_read_parquet, mock_insert):

        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine

        load('test_table', if_exists='append')

        mock_get_files.assert_called_with('/processed',
                                          endswith='.parquet.gzip')
        self.assertEqual(mock_read_parquet.call_count, 2)
        self.assertEqual(mock_insert.call_count, 2)
        mock_engine.connect.assert_called_once()

    @patch(f'{module}.insert_into_db')
    @patch(f'{module}.pd.read_parquet', return_value=MagicMock())
    @patch(f'{module}.get_files_from_dir',
           return_value=["file1.parquet", "file2.parquet"])
    @patch(f'{module}.create_db_engine')
    @patch(f'{module}.config.PROCESSED_DIR', '/processed')
    def test_load_with_custom(self, mock_create_engine, mock_get_files,
                          mock_read_parquet, mock_insert):
        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine

        load('test_table', custom_dir='/custom')

        mock_get_files.assert_called_with('/custom', endswith='.parquet.gzip')
        self.assertEqual(mock_read_parquet.call_count, 2)
        self.assertEqual(mock_insert.call_count, 2)
        mock_engine.connect.assert_called_once()

    @patch(f'{module}.create_db_engine')
    def test_load_engine_failure(self, mock_create_engine):
        mock_create_engine.side_effect = AttributeError('Missing user info')

        with self.assertRaises(RuntimeError) as context:
            load('test_table')
            self.assertIn('Failed to create database',
                          str(context.exception))

    @patch(f'{module}.create_db_engine')
    @patch(f'{module}.get_files_from_dir')
    def test_load_file_read_failure(self, mock_load_files,
                                    mock_create_database):
        mock_load_files.side_effect = Exception('Folder not found')

        with self.assertRaises(RuntimeError) as context:
            load('table_test')
            self.assertIn('Failed to load file list',
                          str(context.exception))

    @patch(f'{module}.create_db_engine')
    @patch(f'{module}.get_files_from_dir',
           return_value=['file1.parquet', 'file2.parquet'])
    @patch(f'{module}.insert_into_db')
    def test_load_database_failure(self, mock_insert, mock_load,
                                   mock_create):
        mock_insert.side_effect = Exception('Failed to find insert')

        with warnings.catch_warnings(record=True) as w:
            load('test_table')
            self.assertEqual(len(w), 2)
            self.assertIn('Failed to load',
                          str(w[0].message))
            self.assertIn('Failed to load',
                          str(w[1].message))


if __name__ == '__main__':
    unittest.main()
