import warnings

import pandas as pd
import sqlalchemy

from etlsus import config
from etlsus.files import get_files_from_dir


def load(
        database_engine: sqlalchemy.engine.base.Engine,
        table_name: str,
        verbose: bool = False,
        infix: str = None,
        **kwargs
) -> None:
    """
    Main load function. Inserts every processed files into
    the select database
    """
    file_dir = config.PROCESSED_DIR
    file_list = get_files_from_dir(
        file_dir, extension='.parquet.gzip', infix=infix
    )

    with database_engine.connect() as conn:
        for file in file_list:
            if verbose:
                print(f'Loading {file} onto the database')

            try:
                df = pd.read_parquet(file)
                with conn.begin():
                    df.to_sql(table_name, conn, **kwargs)
            except Exception as e:
                warnings.warn(f'Failed to load {file}: {e}')

    if verbose:
        print('Finished loading files')
