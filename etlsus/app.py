from typing import Literal

import sqlalchemy
from hydra import compose, initialize

from etlsus import extract, transform, load


def pipeline(
        dataset: Literal['SINASC', 'SIM'],
        years_to_extract: list = None,

        formalize_columns: bool = True,
        formalize_dtype: bool = True,
        formalize_values: bool = True,
        ignored_values: bool = True,
        fix_dates: bool = True,

        database_engine: sqlalchemy.engine.base.Engine = None,
        table_name: str = None,

        verbose: bool = False,
        **kwargs,
):
    """Main pipeline function"""
    with initialize(version_base=None, config_path='./conf'):
        cfg = compose(config_name='config')

        if dataset == 'SINASC' or dataset == 'SIM':
            extract(
                cfg.extract[dataset],
                years_to_extract,
                verbose=verbose
            )

            transform(
                cfg.transform[dataset],
                formalize_columns,
                formalize_dtype,
                formalize_values,
                ignored_values,
                fix_dates,
                infix=cfg.extract[dataset]['prefix'],
                verbose=verbose,
            )

            if table_name and database_engine:
                load(
                    database_engine,
                    table_name,
                    verbose=verbose,
                    infix=cfg.extract[dataset]['prefix'],
                    **kwargs
                )
