from pathlib import Path

from etlsus.files import get_files_from_dir, get_file_name

from etlsus import config
from .processor import FileProcessor


def transform(
        cfg_trans,
        formalize_columns: bool,
        formalize_dtype: bool,
        formalize_values: bool,
        ignored_values: bool,
        fix_dates: bool,
        infix: str = None,
        verbose: bool = False,
) -> None:
    """
    Transforms all unprocessed CSV files in the raw directory using
    configuration files.
    """
    raw_folder = config.RAW_DIR
    processed_folder = config.PROCESSED_DIR
    final_extension = '.parquet.gzip'

    raw_files = get_files_from_dir(raw_folder, '.csv', infix=infix)

    for raw_file in raw_files:
        file_name = get_file_name(raw_file, raw_folder)

        processed_file = (
            processed_folder / Path(file_name).with_suffix(final_extension)
        )

        if not processed_file.exists():
            if verbose:
                print(f'Transforming file: {raw_file}')

            processor = FileProcessor(raw_file, cfg_trans)
            processor.pipeline(
                cfg_trans,
                formalize_columns,
                formalize_dtype,
                formalize_values,
                ignored_values,
                fix_dates,
            )
            processor.save(final_extension)

    if verbose:
        print('Finished transforming files')
