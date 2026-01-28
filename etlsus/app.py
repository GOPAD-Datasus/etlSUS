from typing import Literal

import sqlalchemy
from hydra import compose, initialize

from etlsus import extract, transform, load, merger, config
from .files import get_files_from_dir


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

        merge_at_end: bool = None,

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

            if merge_at_end:
                return merger(infix=cfg.extract[dataset]['prefix'])
            else:
                return get_files_from_dir(
                    config.PROCESSED_DIR,
                    '.gzip',
                    infix=cfg.extract[dataset]['prefix']
                )
        else:
            raise ValueError('Dataset must be "SIM" or "SINASC"')
