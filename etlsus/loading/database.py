import pandas as pd
from sqlalchemy.engine import Engine, Connection
from sqlalchemy import create_engine

from config import get_database_config


def create_db_engine() -> Engine:
    """
    Utilizes 'user', 'password', 'host', 'port' and 'db'
    to create a database engine

    return:
        Engine: sqlalchemy object
    """
    db_configs = get_database_config()

    user = db_configs['USER']
    password = db_configs['PASSWORD']
    host = db_configs['HOST']
    port = db_configs['PORT']
    db = db_configs['DB']

    return create_engine(
        f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}'
    )


def insert_into_db (conn: Connection,
                    df: pd.DataFrame,
                    table_name: str,
                    **kwargs) -> None:
    """
    Insert data into the database. Can be configured with
    additional parameters using kwargs

    params:
        conn (Connection): Valid sqlalchemy object
        df (pd.DataFrame): Dataframe containing the desired data
        table_name (str): Name of the table for insertion
        kwargs: Additional parameters for to_sql
    """
    df.to_sql(table_name, con=conn, **kwargs)
