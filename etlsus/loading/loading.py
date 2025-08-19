import warnings

import pandas as pd

import config
from .database import create_db_engine, insert_into_db
from etlsus.files import get_files_from_dir


def load(table_name: str, **kwargs) -> None:
    """
    Main load function. Inserts every processed files into
    the select database

    param:
        table_name (str): Name of the table inside the db
        kwargs: Additional parameters for to_sql method.
            For more information about said parameters visit:
            https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_sql.html
    """
    try:
        engine = create_db_engine()
    except (AttributeError, ImportError) as e:
        raise RuntimeError(f'Failed to create database'
                           f' engine: {str(e)}') from e

    try:
        file_list = get_files_from_dir(config.PROCESSED_DIR,
                                       endswith='.parquet')
        if not file_list:
            warnings.warn('No parquet files found in processed directory')
            return
    except Exception as e:
        raise RuntimeError(f'Failed to load file list: {str(e)}') from e

    with engine.connect() as conn:
        for item in file_list:
            try:
                df = pd.read_parquet(item)
                with conn.begin():
                    insert_into_db(conn, df,
                                   table_name, **kwargs)
            except Exception as e:
                warnings.warn(f'Failed to load {item}: {e}')
