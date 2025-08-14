import pandas as pd
from sqlalchemy.engine import Engine, Connection
from sqlalchemy import create_engine

import config


def create_db_engine() -> Engine:
    user = config.USER
    password = config.PASSWORD
    host = config.HOST
    port = config.PORT
    db = config.DB

    return create_engine(
        f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"
    )


def insert_into_db (conn: Connection,
                    df: pd.DataFrame,
                    table_name: str,
                    **kwargs) -> None:
    df.to_sql(table_name, con=conn, **kwargs)
