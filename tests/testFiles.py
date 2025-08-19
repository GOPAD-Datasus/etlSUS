import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch

import files


class TestFiles(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_path = self.test_dir.name

    def tearDown(self):
        self.test_dir.cleanup()

    def test_check_file_exists(self):
        test_file = Path(self.test_path) / 'test.txt'
        test_file.touch()
        self.assertTrue(files.check_file_exists(test_file))

        non_existent = Path(self.test_path) / 'none.txt'
        self.assertFalse(files.check_file_exists(non_existent))

        self.assertTrue(files.check_file_exists(str(test_file)))
        self.assertFalse(files.check_file_exists(str(non_existent)))

    @patch('files.config.PROCESSED_DIR', '/processed/')
    @patch('files.check_file_exists')
    def test_check_if_processed(self, mock_check_file):
        mock_check_file.return_value = True
        raw_path = "/raw/data.txt"
        result = files.check_if_processed(raw_path)
        self.assertTrue(result)

        expected_path = Path('/processed/data.parquet.gzip').resolve()
        mock_check_file.assert_called_with(expected_path)

        mock_check_file.return_value = False
        result = files.check_if_processed(raw_path)
        self.assertFalse(result)

    def test_get_files_from_dir(self):
        ext = '.txt'
        file1 = Path(self.test_path) / 'a.txt'
        file2 = Path(self.test_path) / 'b.txt'
        file3 = Path(self.test_path) / 'c.log'
        file1.touch()
        file2.touch()
        file3.touch()

        result = files.get_files_from_dir(self.test_path, ext)
        expected = [str(file1), str(file2)]
        self.assertCountEqual(result, expected)

    @patch('files.config.INPUT_DIR', '/input/')
    def test_get_config_file_found(self):

        with patch('os.walk') as mock_walk:
            mock_walk.return_value = [
                ('/input/subdir', [], ['data.yaml']),
            ]
            result = files.get_config_file('/raw/data.csv')
            self.assertEqual(result,
                             Path('/input/subdir/data.yaml').resolve())

    @patch('files.config.INPUT_DIR', '/input/')
    def test_get_config_file_not_found(self):
        with patch('os.walk') as mock_walk:
            mock_walk.return_value = [
                ('/input/subdir', [], ['other.yaml']),
            ]
            result = files.get_config_file('/raw/data.csv')
            self.assertIsNone(result)

    @patch('files.config.INPUT_DIR', '/input/')
    def test_get_config_file_multiple_dirs(self):
        with patch('os.walk') as mock_walk:
            mock_walk.return_value = [
                ('/input/first', [], []),
                ('/input/second', [], ['data.yaml']),
            ]
            result = files.get_config_file('/raw/data.csv')
            self.assertEqual(result,
                             Path('/input/second/data.yaml').resolve())


if __name__ == '__main__':
    unittest.main()
