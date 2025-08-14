import pandas as pd

import config
from .database import create_db_engine, insert_into_db
from files import load_files


def load(table_name, **kwargs):
    engine = create_db_engine()

    file_list = load_files(config.PROCESSED_DIR, endswith='.parquet')

    with engine.connect() as conn:
        for item in file_list:
            try:
                df = pd.read_parquet(item)
                with conn.begin():
                    insert_into_db(conn, df,
                                   table_name, **kwargs)
            except Exception as e:
                raise Warning(f'Failed to load {item}: {e}')
