import unittest
import warnings
from unittest.mock import patch
import tempfile
import shutil
from pathlib import Path

import pandas as pd
import numpy as np

from transformation.processor import BaseProcessor


class TestBaseProcessor(unittest.TestCase):
    @patch('transformation.processor.BaseProcessor.get_file_name')
    def setUp(self, mock_get_file_name):
        self.test_dir = tempfile.mkdtemp()
        mock_get_file_name.return_value = 'test'

        self.csv_path = Path(self.test_dir) / 'test.csv'
        self.csv_path.touch(exist_ok=True)
        data = "col1,col2,col3\n1,2,He-/llo\n3,4,W;o]r[l+d"
        with open(self.csv_path, 'w') as f:
            f.write(data)

        self.bp = BaseProcessor(self.csv_path, {})

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test__init__(self):
        self.assertEqual(len(self.bp.df), 2)
        self.assertListEqual(
            list(self.bp.df.columns), ['col1', 'col2', 'col3']
        )

    def test__get_read_variables(self):
        rv = {
            'dtype': {
                'col1': {
                    'dtype': 'str',
                    'file': ['test']
                }
            },
            'sep': {
                ',': ['test']
            },
            'encoding': {
                'utf-8': ['test']
            }
        }

        res = self.bp._get_read_variables(rv)
        expected = {'dtype': {'col1': 'str'}, 'sep': ',', 'encoding': 'utf-8'}

        self.assertEqual(res, expected)

    def test_save(self):
        with patch(
            'transformation.processor.BaseProcessor.PROCESSED_DIR',
            self.test_dir
        ):
            self.bp.save('.parquet.gzip')
            output_path = Path(self.test_dir) / 'test.parquet.gzip'

            self.assertTrue(output_path.exists())

            df = pd.read_parquet(output_path)
            pd.testing.assert_frame_equal(df, self.bp.df)

    def test_col_add(self):
        self.bp.col_add(['new_col'])
        self.assertIn('new_col', self.bp.df.columns)
        self.assertTrue(self.bp.df['new_col'].isna().all())

    def test_col_remove(self):
        self.bp.col_remove(['col1'])
        self.assertNotIn('col1', self.bp.df.columns)

    def test_col_rename_dict(self):
        self.bp.col_rename({'col1': 'new_col1', 'col2': 'new_col2'})
        self.assertListEqual(
            list(self.bp.df.columns), ['new_col1', 'new_col2', 'col3']
        )

    def test_col_rename_str(self):
        self.bp.col_rename(str.upper)
        self.assertListEqual(
            list(self.bp.df.columns), ['COL1', 'COL2', 'COL3']
        )

    def test_col_reorder(self):
        self.bp.col_reorder(['col2', 'col1'])  # col3 is removed by method
        self.assertListEqual(
            list(self.bp.df.columns), ['col2', 'col1']
        )

    def test_value_impute(self):
        self.bp.col_add(['col_new'])
        self.bp.value_impute(['col_new'])
        self.assertEqual(self.bp.df['col_new'].isna().sum(), 0)

    def test_value_remove(self):
        self.bp.value_remove({'col1': 1})
        self.assertTrue(self.bp.df['col1'].isna().any())

    def test_value_replace(self):
        self.bp.value_replace({'col1': {1: 99}})
        self.assertEqual(self.bp.df['col1'].iloc[0], 99)

    def test_value_str_translate(self):
        self.bp.value_str_translate({'col3': '-/;][+'})

        self.assertEqual(['Hello', 'World'], self.bp.df['col3'].to_list())

    def test_dtype_change_success(self):
        self.bp.col_add(['col_new'])

        self.bp.dtype_change({'col_new': 'int'})
        self.assertEqual(self.bp.df['col_new'].dtype, int)

    def test_dtype_change_failure(self):
        with warnings.catch_warnings(record=True) as w:
            self.bp.dtype_change({'col3': 'float'})

        self.assertIn(
            'Dtype change not possible', str(w[0].message)
        )

    def test_dtype_optimization(self):
        self.bp.df = self.bp.df.astype(
            {'col1': 'int64', 'col2': 'float64'})
        self.bp.dtype_optimization()
        self.assertTrue(
            np.issubdtype(self.bp.df['col1'].dtype, np.integer))
        self.assertTrue(
            np.issubdtype(self.bp.df['col2'].dtype, np.floating))

    def test_dtype_datetime(self):
        values = {
            'date': ['01-10-2010', '10-05-2010', '31-12-1999'],
            'hour': ['0110', '2354', '2001']
        }
        self.bp.df = pd.DataFrame(values)

        target = {
            'date': '%d-%m-%Y',
            'hour': '%H%M'
        }
        self.bp.dtype_datetime(target)

        df_expected = pd.DataFrame({
            'date': pd.to_datetime(['01-10-2010', '10-05-2010', '31-12-1999'],
                                   format='%d-%m-%Y'),
            'hour': pd.to_datetime(['01:10', '23:54', '20:01'],
                                   format='%H:%M')
        })
        df_expected['hour'] = df_expected['hour'].dt.time

        pd.testing.assert_frame_equal(self.bp.df, df_expected)


if __name__ == '__main__':
    unittest.main()
