from typing import Tuple

import yaml


def get_yaml_urls (input_file_url: str) -> Tuple[dict, str]:
    """
    Load information inside input.yaml

    param:
        input_file_url (str): path to the input file
    returns:
        tuple: Dict of urls for download, prefix for file naming
    raises:
        RuntimeError: If .yaml isn't found or has incorrect structure
    """
    try:
        with open (input_file_url) as f:
            loaded_yaml = yaml.safe_load(f)

            try:
                prefix = loaded_yaml['prefix']
            except KeyError:
                error_msg = (f'Missing prefix value'
                             f' inside yaml')
                raise RuntimeError(error_msg)

            try:
                files = loaded_yaml['files']
            except KeyError:
                error_msg = (f'Missing files section'
                             f' inside yaml')
                raise RuntimeError(error_msg)

            return files, prefix

    except FileNotFoundError:
        error_msg = f'File path {input_file_url} incorrect'
        raise RuntimeError(error_msg)

    except yaml.YAMLError:
        error_msg = f'Incorrect Yaml structure in {input_file_url}'
        raise RuntimeError(error_msg)
