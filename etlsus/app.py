from typing import Literal

from hydra import compose, initialize

from etlsus import extract, transform, load


def pipeline(
        dataset: Literal['SINASC', 'SIM'],

        formalize_columns: bool,
        formalize_dtype: bool,
        formalize_values: bool,
        ignored_values: bool,
        fix_dates: bool,

        file_prefix: str = None,

        table_name: str = None,
        custom_dir: str = None,
        verbose: bool = False,
        **kwargs,
):
    """Main pipeline function"""
    with initialize(version_base=None, config_path='./conf'):
        cfg = compose(config_name='config')

        if dataset == 'SINASC' or dataset == 'SIM':
            extract(cfg.extract[dataset], verbose=verbose)

            transform(
                cfg.transform[dataset],
                formalize_columns,
                formalize_dtype,
                formalize_values,
                ignored_values,
                fix_dates,
                verbose=verbose,
            )

        if table_name:
            load(table_name, verbose, custom_dir=custom_dir, **kwargs)
