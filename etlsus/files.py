from __future__ import annotations

import os
from pathlib import Path
from typing import List, Callable, Union

import config


def check_file_exists(file_path: str | Path) -> bool:
    """
    Checks if a file exists at the specified path.

    param:
        file_path (str | Path): Path to the file to check
    returns:
        bool: True if file exists, False otherwise
    raises:
        OSError: If there are permission issues accessing the file system
    """
    return os.path.isfile(file_path)


def check_if_processed(raw_file_path: str | Path) -> bool:
    """
    Checks if a raw file has already been processed by looking
    for corresponding parquet file.

    param:
        raw_file_path (str | Path): Path to the raw file to check
    returns:
        bool: True if processed file exists, False otherwise
    raises:
        OSError: If there are permission issues accessing the file system
        ValueError: If the raw file path is malformed
    """
    file_name, _ = os.path.basename(raw_file_path).split('.')

    extension = '.parquet.gzip'
    file = Path(str(config.PROCESSED_DIR) +
                f'/{file_name}{extension}').resolve()

    return check_file_exists(file)


def get_files_from_dir(folder_dir: str, endswith: str) -> List[str]:
    """
    Retrieves all files from a directory that match the specified extension.

    param:
        folder_dir (str): Directory path to search for files
        endswith (str): File extension to filter by (e.g., '.csv', '.yaml')
    returns:
        List[str]: List of full file paths matching the criteria
    raises:
        OSError: If the directory doesn't exist or has permission issues
        FileNotFoundError: If the specified directory cannot be found
    """
    return [os.path.join(folder_dir, f)
            for f in os.listdir(folder_dir)
            if f.endswith(endswith)]


def get_config_file(raw_file_path: str | Path) -> Union[Path, None]:
    """
    Finds the corresponding YAML configuration file for a given raw file.

    param:
        raw_file_path (str | Path): Path to the raw file
    returns:
        Union[Path, None]: Path to the configuration file if found, None otherwise
    raises:
        OSError: If there are permission issues accessing the file system
        ValueError: If the raw file path is malformed
    """
    file_name, _ = os.path.basename(raw_file_path).split('.')
    file_name += '.yaml'

    input_dir = config.INPUT_DIR

    for root, dirs, files in os.walk(input_dir):
        if file_name in files:
            return Path(os.path.join(root, file_name)).resolve()
