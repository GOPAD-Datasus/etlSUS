import warnings
from pathlib import Path
from typing import List

import yaml

from etlsus import config
from etlsus.files import get_files_from_dir
from .handlers import Handler


def apply_transformations(transformations_input: dict, handler):
    """
    Applies a series of transformations to a dataframe using handler methods.

    param:
        transformations_input (dict): Dictionary where keys are method
                                      names and values are arguments
                                      for those methods
        handler (Handler): Handler object containing transformation methods
    returns:
        None: This function modifies the handler object in place
    raises:
        Warning: If method names are incorrect or transformations cannot
                 be applied
    """
    for method_name, method_args in transformations_input.items():
        method = getattr(handler, method_name,
                         f'Incorrect method name: {method_name}')

        if type(method) is str:
            warnings.warn(method)
        else:
            if method == handler.optimize_dtype:
                method()
            else:
                method(method_args)


def transform_file(raw_file: str, generic_path: str = None) -> None:
    """
    Transforms a CSV file based on YAML configuration and optional
    generic transformations.

    param:
        raw_file (str): Path to the raw CSV file to be transformed
        generic_path (str, optional): Path to generic YAML file with
                                      additional transformations
    returns:
        None: Saves the transformed file to processed directory
    raises:
        RuntimeError: If YAML file is not found or has incorrect structure
        KeyError: If required keys are missing in the configuration
        Warning: If transformations cannot be applied correctly
    """

    config_file = get_files_from_dir(config.INPUT_DIR,
                                     Path(raw_file).with_suffix('.yaml').name)

    if isinstance(config_file, List):
        config_file = config_file[0]

    try:
        with open(config_file) as f:
            info = yaml.safe_load(f)
    except (TypeError, FileNotFoundError):
        error_msg = f'No yaml file found for {raw_file}'
        raise RuntimeError(error_msg)
    except yaml.YAMLError:
        error_msg = f'Incorrect Yaml structure in {config_file}'
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
