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

    param:
        database_engine (Engine): SqlAlchemy engine object
        table_name (str): Name of the table inside the db
        verbose (bool): Whether to print the full summary of execution
        kwargs: Additional parameters for df.to_sql method.
            For more information about said parameters visit:
            https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_sql.html
    raises:
        RuntimeError: If not able to create a database engine or find
                      the list of processed files
        Warning: If list of processed files is empty or fails to load a
                 file into database
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
