import os
import warnings
from urllib.request import urlretrieve

from etlsus import config
from .utils import get_yaml_urls
from etlsus.files import check_file_exists


def extract(input_file_url: str, verbose: bool = False) -> None:
    """
    Main extraction function. Downloads from every url
    inside the files key from input.yaml file.

    param:
        input_file_url (str): Path to the yaml file
        verbose (bool): Whether to print the full summary of execution
    raises:
        Warning: If urlretrieve fails to download a file
    """
    raw_folder = config.RAW_DIR
    extension = '.csv'

    files, prefix = get_yaml_urls(input_file_url)

    for year in files.keys():
        source_link = files[year]
        output_file = os.path.join(raw_folder,
                                   f'{prefix}{year}{extension}')

        if not check_file_exists(output_file):
            if verbose:
                print(f'Downloading: {source_link}\n'
                      f' ↳ Saving at: {output_file}')

            try:
                urlretrieve(source_link,
                            output_file)
            except Exception as e:
                error_msg = (
                    f'Failed to download {year}: {e}\n'
                    f'Please verify the url in input.yaml'
                )
                warnings.warn(error_msg)

    if verbose:
        print('Finished downloading files')
