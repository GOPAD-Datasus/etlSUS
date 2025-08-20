import unittest
from unittest.mock import patch

from etlsus.extraction.utils import get_yaml_urls


class TestUtils(unittest.TestCase):

    @patch('builtins.open')
    @patch('etlsus.extraction.utils.yaml.safe_load')
    def test_get_yaml_urls_correct(self, mock_safe_load, _):
        
        mock_safe_load.return_value = (
            {
                'files':  {1: 'abc', 2: 'foo', 3: 'bar'},
                'prefix': 'TEST'
            }
        )

        expected_result = ({1: 'abc', 2: 'foo', 3: 'bar'},
                           'TEST')

        correct = 'dummy_input.yaml'
        self.assertEqual(get_yaml_urls(correct),
                         expected_result)

    @patch('builtins.open')
    @patch('etlsus.extraction.utils.yaml.safe_load')
    def test_get_yaml_urls_incorrect(self, mock_safe_load, _):
        mock_safe_load.return_value = {}

        faulty = 'dummy_input.yaml'
        self.assertRaises(RuntimeError,
                          get_yaml_urls,
                          faulty)

    def test_get_yaml_urls_missing(self):
        missing = '../wrong/file.yaml'

        self.assertRaises(RuntimeError,
                          get_yaml_urls,
                          missing)


if __name__ == '__main__':
    unittest.main()
