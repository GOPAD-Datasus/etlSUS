from __future__ import annotations

import os
from pathlib import Path
from typing import List

import config


def check_file_exists(file_path: str | Path) -> bool:
    """
    Returns True if a file exists. False if otherwise.

    param:
        path (str): Path leading to the file
    return:
        bool: State of the file
    """
    return os.path.isfile(file_path)


def check_if_processed(raw_file_path: str | Path) -> bool:
    file_name, _ = os.path.basename(raw_file_path).split('.')

    extension = '.parquet.gzip'
    file = Path(config.PROCESSED_DIR + file_name + extension).resolve()

    return check_file_exists(file)


def get_files_from_dir(folder_dir: str, endswith: str) -> List[str]:
    return [os.path.join(folder_dir, f)
            for f in os.listdir(folder_dir)
            if f.endswith(endswith)]


def get_config_file(raw_file_path: str | Path) -> str | None:
    file_name, _ = os.path.basename(raw_file_path).split('.')
    file_name += '.yaml'

    input_dir = config.INPUT_DIR

    for root, dirs, files in os.walk(input_dir):
        if file_name in files:
            return os.path.join(root, file_name)
