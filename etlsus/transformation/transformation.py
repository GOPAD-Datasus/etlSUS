from pathlib import Path

from etlsus.files import get_files_from_dir, file_exists, get_file_name

from etlsus.config import RAW_DIR, PROCESSED_DIR
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
    raw_folder = RAW_DIR
    processed_folder = PROCESSED_DIR
    final_extension = '.parquet.gzip'

    raw_files = get_files_from_dir(raw_folder, '.csv', infix=infix)

    for raw_file in raw_files:
        file_name = get_file_name(raw_file, RAW_DIR)

        processed_file = (
            processed_folder / Path(file_name).with_suffix(final_extension)
        )

        if not file_exists(processed_file):
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
