import warnings

import pandas as pd

import config
from .database import create_db_engine, insert_into_db
from etlsus.files import get_files_from_dir


def load(table_name: str, verbose: bool = False, **kwargs) -> None:
    """
    Main load function. Inserts every processed files into
    the select database

    param:
        table_name (str): Name of the table inside the db
        verbose (bool): Whether to print the full summary of execution
        kwargs: Additional parameters for to_sql method.
            For more information about said parameters visit:
            https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_sql.html
    raises:
        RuntimeError: If not able to create a database engine or find
                      the list of processed files
        Warning: If list of processed files is empty or fails to load a
                 file into database
    """
    try:
        engine = create_db_engine()
    except (AttributeError, ImportError) as e:
        raise RuntimeError(f'Failed to create database'
                           f' engine: {str(e)}') from e

    try:
        file_list = get_files_from_dir(config.PROCESSED_DIR,
                                       endswith='.parquet.gzip')
        if not file_list:
            msg = (f'No parquet files found in processed directory: '
                   f'{config.PROCESSED_DIR}')
            warnings.warn(msg)
            return
    except Exception as e:
        raise RuntimeError(f'Failed to load file list: {str(e)}') from e

    with engine.connect() as conn:
        for item in file_list:
            if verbose:
                print(f'Loading {item} onto the database')

            try:
                df = pd.read_parquet(item)
                with conn.begin():
                    insert_into_db(conn, df,
                                   table_name, **kwargs)
            except Exception as e:
                warnings.warn(f'Failed to load {item}: {e}')

    if verbose:
        print('Finished loading files')
