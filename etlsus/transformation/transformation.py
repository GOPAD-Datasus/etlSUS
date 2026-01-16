from pathlib import Path

from .mapper import transform_file
from etlsus.files import get_files_from_dir, file_exists

from etlsus import config


def transform(generic_yaml_file: str = None, verbose: bool = False) -> None:
    """
    Transforms all unprocessed CSV files in the raw directory using
    configuration files.

    param:
        generic_yaml_file (str, optional): Path to generic YAML file
                                           for additional transformations
        verbose (bool): Whether to print the full summary of execution
    returns:
        None: Processes and saves all unprocessed files
    raises:
        RuntimeError: If any file transformation fails
        Warning: If individual file transformations encounter issues
    """
    raw_folder = config.RAW_DIR
    processed_folder = config.PROCESSED_DIR
    final_extension = '.parquet'

    raw_files = get_files_from_dir(raw_folder, '.csv')

    for raw_file in raw_files:
        processed_file = (processed_folder
                          / Path(raw_file).with_suffix(final_extension).name)

        if not file_exists(processed_file):

            if verbose:
                print(f'Transforming file: {raw_file}')

            transform_file(raw_file, generic_yaml_file)

    if verbose:
        print('Finished transforming files')
