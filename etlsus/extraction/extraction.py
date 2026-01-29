import shutil
import warnings
from pathlib import Path
from urllib.request import urlretrieve

from etlsus import config


def extract(
        cfg: dict,
        years_to_extract: list = None,
        verbose: bool = False
) -> None:
    """
    Main extraction function. Downloads urls inside
    the 'files' key in download_urls.

    param:
        cfg (Dict): URL to files and Prefix for files
        years_to_extract (List): List of years to extract
        verbose (bool): Whether to print the full summary of execution
    raises:
        Warning: If urlretrieve fails to download a file
    """
    for year, file in cfg['files'].items():
        if years_to_extract and year not in years_to_extract:
            continue

        file_name = Path(f'{cfg["prefix"]}{year}{Path(file).suffix}')
        output_path = Path(config.RAW_DIR) / file_name

        if not output_path.exists():
            if verbose:
                print(f'Downloading year: {year}\n'
                      f' ↳ Saving at: {output_path}')
            try:
                urlretrieve(file, output_path)
            except Exception as e:
                error_msg = f'Failed to download {year}: {e}\n'
                warnings.warn(error_msg)

        if output_path.suffix == '.zip':
            unzip_dir_path = output_path.with_suffix('')

            if unzip_dir_path.exists():
                continue

            unzip_dir_path.mkdir()
            shutil.unpack_archive(output_path, unzip_dir_path)

    if verbose:
        print('Finished downloading files')
