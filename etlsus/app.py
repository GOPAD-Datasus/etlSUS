import os
from pathlib import Path
from typing import Literal, Union, List

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
) -> Union[Path, List[Path]]:
    """
    Main pipeline function for extracting, transforming, and loading data.

    This function downloads data from the specified dataset and years, applies
    transformations, and loads it into a database. Can optionally merge all
    processed files into a single file at the end.

    Important behaviors:
    1. Database loading can be disabled by omitting 'database_engine'
       and 'table_name'
    2. File merging can be disabled by omitting 'merge_at_end'
    3. Returns List[Path] if both database loading and merging are disabled

    Parameters
    ----------
    dataset : SINASC or SIM
        Dataset to download data from
    base_dir : Path
        Base directory for downloaded files
    years_to_extract : List[int]
        Years to download

    formalize_columns : bool, default=False
        Whether to formalize column names
    formalize_dtype : bool, default=False
        Whether to formalize data types
    formalize_values : bool, default=False
        Whether to formalize values
    ignored_values : bool, default=False
        Whether to remove 'ignored' values
    fix_dates : bool, default=False
        Whether to fix date formats

    database_engine : Engine, optional
        SQLAlchemy engine object (required for database loading)
    table_name : str, optional
        Target table name (required for database loading)
    **kwargs : dict, optional
        Additional parameters for pandas.DataFrame.to_sql() See:
        https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_sql.html

    merge_at_end : bool, default=False
        Whether to merge all processed files into a single file
    verbose : bool, default=False
        Whether to print detailed execution summary

    Returns
    -------
    List[Path] or Path
    List of file paths if both load and merge are disabled,
    otherwise merged file Path

    Raises
    ------
    Warning
        If the pipeline fails to download a file
    """
    os.environ['ETLSUS_BASE_DIR'] = base_dir

    from .pipeline import run_pipeline

    return run_pipeline(
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
