import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from etlsus.loading import merger


class TestMerger(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_path = Path(self.test_dir.name)

        self.config_patch = patch('etlsus.loading.merge.config')
        self.mock_config = self.config_patch.start()
        self.mock_config.PROCESSED_DIR = self.test_path / 'processed'
        self.mock_config.DATA_DIR = self.test_path / 'data'

        self.mock_config.PROCESSED_DIR.mkdir(parents=True)
        self.mock_config.DATA_DIR.mkdir(parents=True)

        df = pd.DataFrame({
            'col1': [1, 2, 3],
            'col2': [4, 5, 6],
        })
        table = pa.Table.from_pandas(df)
        self.file_1 = self.mock_config.PROCESSED_DIR / 'table.parquet'
        pq.write_table(table, self.file_1)

        df = pd.DataFrame({
            'col1': [7, 8],
            'col2': [9, 0],
        })
        table = pa.Table.from_pandas(df)
        self.file_2 = self.mock_config.PROCESSED_DIR / 'table_2.parquet'
        pq.write_table(table, self.file_2)

        df = pd.DataFrame({
            'col3': ['foo', 'bar'],
        })
        table = pa.Table.from_pandas(df)
        self.incompatible = self.mock_config.PROCESSED_DIR / 'incomp.parquet'
        pq.write_table(table, self.incompatible)

    def tearDown(self):
        self.test_dir.cleanup()

    @patch('etlsus.loading.merge.get_files_from_dir')
    def test_merge_successful(self, mock_get_files_from_dir):
        mock_get_files_from_dir.return_value = [self.file_1, self.file_2]

        output_path = merger('test')

        expected = {
            'col1': [1, 2, 3, 7, 8],
            'col2': [4, 5, 6, 9, 0],
        }
        df_expected = pd.DataFrame(expected)

        self.assertTrue(output_path.exists())

        df = pd.read_parquet(output_path)
        pd.testing.assert_frame_equal(df, df_expected)

    @patch('etlsus.loading.merge.get_files_from_dir')
    def test_merge_failed(self, mock_get_files_from_dir):
        mock_get_files_from_dir.return_value = [self.file_1, self.incompatible]

        with self.assertRaises(ValueError):
            merger('test')

        expected_output_path = self.mock_config.DATA_DIR / 'test.parquet.gzip'
        self.assertFalse(expected_output_path.exists())

    @patch('etlsus.loading.merge.get_files_from_dir')
    @patch('etlsus.loading.merge.pq')
    def test_merge_correct_output_exists(
            self, mock_pq, mock_get_files_from_dir
    ):
        mock_get_files_from_dir.return_value = []

        mock_path = MagicMock()
        mock_path.exists.return_value = True
        self.mock_config.DATA_DIR = mock_path

        mock_read_metadata = MagicMock()
        mock_read_metadata.num_rows = 0
        mock_pq.read_metadata.return_value = mock_read_metadata

        mock_parquet_writer_instance = MagicMock()
        mock_pq.ParquetWriter.return_value = mock_parquet_writer_instance

        merger('test')

        mock_parquet_writer_instance.assert_not_called()

    @patch('etlsus.loading.merge.get_files_from_dir')
    def test_merge_existing_output_different_rowcount(
            self, mock_get_files_from_dir
    ):
        mock_get_files_from_dir.return_value = [self.file_1, self.file_2]

        output_path = self.mock_config.DATA_DIR / 'test.parquet.gzip'

        df_incorrect = pd.DataFrame({
            'col1': [1],
            'col2': [2],
        })
        table_incorrect = pa.Table.from_pandas(df_incorrect)
        pq.write_table(table_incorrect, output_path, compression='gzip')

        self.assertTrue(output_path.exists())
        initial_nrows = pq.read_metadata(output_path).num_rows
        self.assertEqual(initial_nrows, 1)

        result_path = merger('test')

        self.assertEqual(result_path, output_path)
        self.assertTrue(result_path.exists())

        final_nrows = pq.read_metadata(result_path).num_rows
        self.assertEqual(final_nrows, 5)

        df_result = pd.read_parquet(result_path)
        expected_df = pd.DataFrame({
            'col1': [1, 2, 3, 7, 8],
            'col2': [4, 5, 6, 9, 0],
        })
        pd.testing.assert_frame_equal(df_result, expected_df)


if __name__ == '__main__':
    unittest.main()
