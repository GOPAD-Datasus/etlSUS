import unittest

import pandas as pd

from etlsus.transformation.handlers.utils.time import TimeHandler


class TestTime(unittest.TestCase):
    def test_get_format_item_length(self):
        format_ = '%f-%S-%M-%H'  # Expected: 15
        time_handler = TimeHandler(format_)
        self.assertEqual(15, time_handler._get_format_item_length())

    def test_correct_length(self):
        date_strs = ['30/02/10', '14/06/100', '01/07/1']
        format_ = '%d/%m/%y'

        time_handler = TimeHandler(format_)

        results = [time_handler._correct_length(x) for x in date_strs]
        expected = ['30/02/10', '14/06/10', pd.NaT]

        self.assertEqual(results, expected)

    def test_convert_date(self):
        date_series = pd.Series(['30/02/10', '14/06/100', '01/07/1'])
        format_ = '%d/%m/%y'

        time_handler = TimeHandler(format_)

        date_series = time_handler.convert_date(date_series)
        expected = pd.Series(
            pd.to_datetime(['30/02/10', '14/06/10', pd.NaT],
                           format=format_,
                           errors='coerce')
        )

        pd.testing.assert_series_equal(date_series, expected)


if __name__ == '__main__':
    unittest.main()
