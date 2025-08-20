import unittest
import warnings
from unittest.mock import patch, MagicMock, mock_open

import yaml

from etlsus.transformation.mapper import apply_transformations, transform_file
from etlsus.transformation.handlers import Handler


class TestMapper(unittest.TestCase):
    module = 'etlsus.transformation.mapper'

    def test_apply_transformations_success(self):
        correct_transformations = {
            'add_cols': ['foo', 'bar']
        }

        mock_handler = MagicMock()

        apply_transformations(correct_transformations, mock_handler)

        mock_handler.add_cols.assert_called_with(['foo', 'bar'])

    @patch('etlsus.transformation.handlers.handler.pd.read_csv',
           return_value=MagicMock())
    def test_apply_transformations_incorrect_method(self, mock_read):
        incorrect_transformations = {
            'cols_add': ['foo', 'bar']
        }

        handler = Handler('mock/path')

        with warnings.catch_warnings(record=True) as w:
            apply_transformations(incorrect_transformations, handler)

            self.assertEqual(len(w), 1)
            self.assertIn('Incorrect method name',
                          str(w[0].message))

    @patch(f'{module}.get_config_file')
    @patch(f'{module}.Handler')
    @patch(f'{module}.apply_transformations')
    @patch('builtins.open', new_callable=mock_open)
    def test_transform_file_success(self, mock_open_file, mock_apply,
                                    mock_handler, mock_get_config):
        mock_get_config.return_value = '/path/to/config.yaml'
        config_data = {
            'read_variables':  {'var1': 'value1'},
            'transformations': [{'add_cols': 'foo'}],
            'name':            'output_name'
        }
        generic_data = [{'add_cols': 'bar'}]

        def file_data(file, *args):
            if file == '/path/to/config.yaml':
                return (mock_open(read_data=yaml.dump(config_data))
                        .return_value)
            elif file == '/path/generic.yaml':
                return (mock_open(read_data=yaml.dump(generic_data))
                        .return_value)
            raise FileNotFoundError(file)

        mock_open_file.side_effect = file_data

        transform_file('raw_file.txt',
                       generic_path='/path/generic.yaml')

        mock_handler.assert_called_once_with('raw_file.txt', var1='value1')
        mock_apply.assert_any_call([{'add_cols': 'foo'}],
                                   mock_handler.return_value)
        mock_apply.assert_any_call([{'add_cols': 'bar'}],
                                   mock_handler.return_value)

        mock_handler.return_value.save.assert_called_once_with('output_name')
        self.assertEqual(mock_open_file.call_count, 2)
        mock_open_file.assert_any_call('/path/to/config.yaml')
        mock_open_file.assert_any_call('/path/generic.yaml')

    @patch(f'{module}.get_config_file')
    @patch('builtins.open', new_callable=mock_open)
    def test_transform_file_missing_required_keys(self, mock_open_file,
                                                  mock_get_config):
        mock_get_config.return_value = '/path/to/config.yaml'
        config_data = {'name': 'test'}

        def file_data(file, *args):
            if file == '/path/to/config.yaml':
                return (mock_open(read_data=yaml.dump(config_data))
                        .return_value)
            raise FileNotFoundError(file)

        mock_open_file.side_effect = file_data

        with self.assertRaises(KeyError) as cm:
            transform_file('raw_file.txt')
        self.assertIn('Missing required keys in config',
                      str(cm.exception))

    @patch(f'{module}.get_config_file')
    @patch('builtins.open', new_callable=mock_open,
           read_data='invalid: yaml: :')
    def test_transform_file_invalid_yaml(self, _, mock_get_config):
        mock_get_config.return_value = '/path/to/config.yaml'
        with self.assertRaises(RuntimeError) as re:
            transform_file('raw_file.txt')

        self.assertIn('Incorrect Yaml structure in',
                      str(re.exception))

    @patch(f'{module}.get_config_file')
    def test_transform_file_invalid_path(self, mock_get_config):
        mock_get_config.return_value = '/path/to/config.yaml'
        with self.assertRaises(RuntimeError):
            transform_file('raw_file.txt')


if __name__ == '__main__':
    unittest.main()
