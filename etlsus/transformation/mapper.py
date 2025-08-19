import warnings

import yaml

from .handlers import Handler
from etlsus.files import get_config_file


def apply_transformations(transformations_input: dict, handler):
    for method_name, method_args in transformations_input.items():
        method = getattr(handler, method_name,
                         f'Incorrect method name: {method_name}')

        if type(method) == str:
            warnings.warn(method)
        else:
            method(method_args)


def transform_file(raw_file: str, generic_path: str = None) -> None:
    config_file_path = get_config_file(raw_file)

    try:
        with open(config_file_path) as f:
            info = yaml.safe_load(f)
    except FileNotFoundError:
        error_msg = f'File path {config_file_path} incorrect'
        raise RuntimeError(error_msg)
    except yaml.YAMLError:
        error_msg = f'Incorrect Yaml structure in {config_file_path}'
        raise RuntimeError(error_msg)

    required_keys = {'read_variables', 'transformations', 'name'}
    if missing := required_keys - info.keys():
        raise KeyError(f"Missing required keys in config: {missing}")

    handler = Handler(raw_file, **info['read_variables'])

    apply_transformations(info['transformations'], handler)

    if generic_path:
        try:
            with open(generic_path) as f:
                generic = yaml.safe_load(f)
        except FileNotFoundError:
            error_msg = f'File path {generic_path} incorrect'
            raise RuntimeError(error_msg)
        except yaml.YAMLError:
            error_msg = f'Incorrect Yaml structure in {generic_path}'
            raise RuntimeError(error_msg)

        apply_transformations(generic, handler)

    handler.save(info['name'])
