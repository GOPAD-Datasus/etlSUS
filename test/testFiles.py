import unittest
import tempfile
from pathlib import Path

from etlsus import files


class TestFiles(unittest.TestCase):
    module = 'etlsus.files'

    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_path = self.test_dir.name

    def tearDown(self):
        self.test_dir.cleanup()

    def test_file_exists_success(self):
        test_file = Path(self.test_path) / 'test_file.txt'
        test_file.touch()
        self.assertTrue(files.file_exists(test_file))
        self.assertTrue(files.file_exists(str(test_file)))

    def test_file_exists_failure(self):
        non_existent = Path(self.test_path) / 'test_file.txt'
        self.assertFalse(files.file_exists(non_existent))
        self.assertFalse(files.file_exists(str(non_existent)))

    def test_get_files_from_dir_success(self):
        ext = '.txt'
        folder = Path(self.test_path) / 'folder'
        folder.mkdir()

        file1 = Path(self.test_path) / 'a.txt'
        file2 = Path(self.test_path) / 'folder' / 'b.txt'
        file3 = Path(self.test_path) / 'c.log'
        file1.touch()
        file2.touch()
        file3.touch()

        result = files.get_files_from_dir(self.test_path, ext)
        expected = [file1, file2]
        self.assertEqual(result, expected)

    def test_get_files_from_dir_failure(self):
        ext = '.txt'

        result = files.get_files_from_dir(self.test_path, ext)
        expected = []

        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
