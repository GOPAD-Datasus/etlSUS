import os
from typing import Literal

import sqlalchemy


def pipeline(
        dataset: Literal['SINASC', 'SIM'],
        base_dir: str,
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
    os.environ['ETLSUS_BASE_DIR'] = base_dir

    from .pipeline import run_pipeline

    run_pipeline(
        dataset=dataset,
        years_to_extract=years_to_extract,

        formalize_columns=formalize_columns,
        formalize_dtype=formalize_dtype,
        formalize_values=formalize_values,
        ignored_values=ignored_values,
        fix_dates=fix_dates,

        database_engine=database_engine,
        table_name=table_name,

        merge_at_end=merge_at_end,

        verbose=verbose,
        **kwargs,
    )
