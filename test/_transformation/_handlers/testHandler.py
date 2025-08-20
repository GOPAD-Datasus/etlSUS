import unittest
import warnings
from unittest.mock import patch
import tempfile
import shutil
import os
from pathlib import Path

import pandas as pd
import numpy as np

from etlsus.transformation import Handler


class TestHandler(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        # Create a sample CSV file
        self.csv_path = os.path.join(self.test_dir, 'test.csv')
        data = "col1,col2,col3\n1,2,foo\n3,4,bar"
        with open(self.csv_path, 'w') as f:
            f.write(data)
        # Initialize Handler
        self.handler = Handler(self.csv_path)

    def tearDown(self):
        # Remove temporary directory after tests
        shutil.rmtree(self.test_dir)

    def test_init(self):
        # Test if DataFrame is loaded correctly
        self.assertEqual(len(self.handler.df), 2)
        self.assertListEqual(list(self.handler.df.columns),
                             ['col1', 'col2', 'col3'])

    def test_save(self):
        with patch('config.PROCESSED_DIR', self.test_dir):
            self.handler.save('test_output')
            output_path = Path(self.test_dir + '/test_output.parquet.gzip')
            # Check if file exists
            self.assertTrue(output_path.exists())
            # Read back and verify data
            df = pd.read_parquet(output_path)
            pd.testing.assert_frame_equal(df, self.handler.df)

    def test_add_cols(self):
        # Add single column
        self.handler.add_cols('new_col')
        self.assertIn('new_col', self.handler.df.columns)
        self.assertTrue(self.handler.df['new_col'].isna().all())

        # Add multiple columns
        self.handler.add_cols(['col4', 'col5'])
        self.assertListEqual(['col4', 'col5'],
                             list(self.handler.df.columns[-2:]))
        self.assertTrue(self.handler.df[['col4', 'col5']].isna().all().all())

    def test_remove_cols(self):
        # Remove single column
        self.handler.remove_cols(['col1'])
        self.assertNotIn('col1', self.handler.df.columns)

        # Remove multiple columns
        self.handler.remove_cols(['col1', 'col2'])  # col1 already removed
        self.assertListEqual(list(self.handler.df.columns), ['col3'])

    def test_rename_cols(self):
        self.handler.rename_cols({'col1': 'new_col1', 'col2': 'new_col2'})
        self.assertListEqual(list(self.handler.df.columns),
                             ['new_col1', 'new_col2', 'col3'])

    def test_organize_cols(self):
        # Reorder columns
        self.handler.organize_cols(['col2', 'col1'])
        self.assertListEqual(list(self.handler.df.columns),
                             ['col2', 'col1'])

    def test_impute_values(self):
        # Add NaN and impute
        self.handler.df.loc[0, 'col1'] = np.nan
        self.handler.impute_values(['col1'])
        self.assertEqual(self.handler.df['col1'].iloc[0], 0)

    def test_remove_values(self):
        # Replace 1 with NaN
        self.handler.remove_values({'col1': 1})
        self.assertTrue(np.isnan(self.handler.df['col1'].iloc[0]))

    def test_replace_values(self):
        # Replace 1 with 99 and 2 with 100
        self.handler.replace_values({'col1': {1: 99}, 'col2': {2: 100}})
        self.assertEqual(self.handler.df['col1'].iloc[0], 99)
        self.assertEqual(self.handler.df['col2'].iloc[0], 100)

    def test_translate_str_simple_input_success(self):
        values = {
            'str_col': ['He-/llo', 'W;o]r[l+d']
        }

        self.handler.df = pd.DataFrame(values)

        self.handler.translate_str({'str_col': '-/;][+'})

        expected = pd.DataFrame({'str_col': ['Hello', 'World']})
        pd.testing.assert_series_equal(expected['str_col'],
                                       self.handler.df['str_col'])

    def test_translate_str_nested_input_success(self):
        values = {
            'str_col': ['12330', 'Wor36']
        }

        self.handler.df = pd.DataFrame(values)

        self.handler.translate_str({'str_col': {'12306': 'Helod'}})

        expected = pd.DataFrame({'str_col': ['Hello', 'World']})
        pd.testing.assert_series_equal(expected['str_col'],
                                       self.handler.df['str_col'])

    def test_change_dtype_success(self):
        self.handler.change_dtype({'col1': 'float'})
        self.assertEqual(self.handler.df['col1'].dtype, float)

    def test_change_dtype_failure(self):
        with warnings.catch_warnings(record=True) as w:
            self.handler.change_dtype({'col3': 'float'})

        self.assertIn('Dtype change not possible',
                      str(w[0].message))

    def test_change_dtype_incorrect_info(self):
        with warnings.catch_warnings(record=True) as w:
            self.handler.change_dtype({'col1': 'datetime'})

            self.assertIn('Incorrect info.',
                          str(w[0].message))

    def test_optimize_dtype(self):
        self.handler.df = self.handler.df.astype(
            {'col1': 'int64', 'col2': 'float64'})
        self.handler.optimize_dtype()
        self.assertTrue(
            np.issubdtype(self.handler.df['col1'].dtype, np.integer))
        self.assertTrue(
            np.issubdtype(self.handler.df['col2'].dtype, np.floating))

    def test_datetime_dtype(self):
        values = {
            'date': ['01-10-2010', '10-05-20100', '31-12-1999'],
            'hour': ['01:10', '23:540', '20:01']
        }

        self.handler.df = pd.DataFrame(values)

        target = {
            'date': '%d-%m-%Y',
            'hour': '%H:%M'
        }

        self.handler.datetime_dtype(target)

        df_expected = pd.DataFrame({
            'date': pd.to_datetime(['01-10-2010', '10-05-2010', '31-12-1999'],
                                   format='%d-%m-%Y'),
            'hour': pd.to_datetime(['01:10', '23:54', '20:01'],
                                   format='%H:%M')
        })
        pd.testing.assert_frame_equal(self.handler.df, df_expected)

    def test_combine_date_with_time_dtype(self):
        self.handler.df = pd.DataFrame({
            'date': pd.to_datetime(['01-10-2010', '10-05-2010', '31-12-1999'],
                                   format='%d-%m-%Y'),
            'hour': pd.to_datetime(['01:10', '23:54', '20:01'],
                                   format='%H:%M')
        })

        self.handler.combine_date_with_time_dtype({'date': 'hour'})

        pd.DataFrame({
            'date': pd.to_datetime(['01-10-2010', '10-05-2010', '31-12-1999'],
                                   format='%d-%m-%Y'),
            'hour': pd.to_datetime(['01:10', '23:54', '20:01'],
                                   format='%H:%M')
        })

        expected_df = pd.DataFrame({
            'date': pd.to_datetime(['01-10-2010 01:10',
                                    '10-05-2010 23:54',
                                    '31-12-1999 20:01'],
                                   format='%d-%m-%Y %H:%M'),
        })

        pd.testing.assert_series_equal(expected_df['date'],
                                       self.handler.df['date'])


if __name__ == '__main__':
    unittest.main()
