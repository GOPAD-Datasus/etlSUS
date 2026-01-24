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

    def test_get_files_from_dir_prefix(self):
        ext = '.txt'
        prefix = 'test'
        folder = Path(self.test_path) / 'test'
        folder.mkdir()

        file_missing = Path(self.test_path) / 'a.txt'
        file_found_1 = Path(self.test_path) / 'test_b.txt'
        file_found_2 = Path(self.test_path) / 'test' / 'c.txt'

        file_missing.touch()
        file_found_1.touch()
        file_found_2.touch()

        result = files.get_files_from_dir(self.test_path, ext, prefix)
        expected = [file_found_1, file_found_2]
        self.assertEqual(result, expected)

    def test_get_file_name_success_no_folder(self):
        excluding_path = Path(self.test_path) / 'raw'
        excluding_path.mkdir()

        file_path = excluding_path / 'file_name.csv'
        file_path.touch()

        result = files.get_file_name(file_path, excluding_path)
        expected = 'file_name'
        self.assertEqual(result, expected)

    def test_get_file_name_success_with_folder(self):
        file_location = Path(self.test_path) / 'raw'
        file_location.mkdir()

        file_path = file_location / 'file_name'
        file_path.mkdir()
        file_path = file_path / 'any_name.csv'
        file_path.touch()

        result = files.get_file_name(file_path, file_location)
        expected = 'file_name'
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
