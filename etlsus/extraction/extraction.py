import os
from urllib.request import urlretrieve

import config
from .utils import get_yaml_urls
from files import check_file_exists


def extract(input_file_url: str) -> None:
    """
    Main extraction function. Downloads from every url
    inside the files key from input.yaml file.

    param:
        input_file_url (str): Path to the yaml file
    """
    raw_folder = config.RAW_DIR
    extension = '.csv'

    files, prefix = get_yaml_urls(input_file_url)

    for year in files.keys():
        source_link = files[year]
        output_file = os.path.join(raw_folder,
                                   f'{prefix}{year}{extension}')

        if not check_file_exists(output_file):
            try:
                urlretrieve(source_link,
                            output_file)
            except Exception as e:
                error_msg = (
                    f'Failed to download {year}: {e}\n'
                    f'Please verify the url in input.yaml'
                )
                print(f'Warning: {error_msg}')
