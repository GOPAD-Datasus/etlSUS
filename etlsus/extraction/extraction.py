import warnings
from pathlib import Path
from urllib.request import urlretrieve

from etlsus import config
from etlsus.files import file_exists


def extract(dataset: dict, verbose: bool = False) -> None:
    """
    Main extraction function. Downloads from every url
    inside the files key from input.yaml file.

    param:
        dataset (Dict): URL to files and Prefix for files
        verbose (bool): Whether to print the full summary of execution
    raises:
        Warning: If urlretrieve fails to download a file
    """
    for year, file in dataset['files'].items():
        file_name = Path(f'{dataset['prefix']}{year}{Path(file).suffix}')
        output_path = Path(config.RAW_DIR) / file_name

        if not file_exists(output_path):
            if verbose:
                print(f'Downloading year: {year}\n'
                      f' ↳ Saving at: {output_path}')
            try:
                urlretrieve(file, output_path)
            except Exception as e:
                error_msg = f'Failed to download {year}: {e}\n'
                warnings.warn(error_msg)

    if verbose:
        print('Finished downloading files')
