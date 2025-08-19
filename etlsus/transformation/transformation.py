from transformation.mapper import transform_file
from files import check_if_processed, get_files_from_dir

import config


def transform(generic_yaml_file: str = None) -> None:
    raw_folder = config.RAW_DIR
    raw_files = get_files_from_dir(raw_folder, '.csv')

    for raw_file in raw_files:
        if not check_if_processed(raw_file):
            transform_file(raw_file, generic_yaml_file)
