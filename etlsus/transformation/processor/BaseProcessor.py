import warnings
from pathlib import Path
from typing import List, Dict

import pandas as pd
import numpy as np

from etlsus import config
from etlsus.files import get_file_name

pd.set_option('future.no_silent_downcasting', True)


class BaseProcessor:
    def __init__(self, url: Path, cfg_rv):
        self.file_name = get_file_name(url, config.RAW_DIR)

        self.df = pd.read_csv(url, **self._get_read_variables(cfg_rv))

    def _get_read_variables(self, cfg_rv) -> dict:
        dtype = {}
        if cfg_rv.get('dtype'):
            dtype = {
                key: dict_['dtype'] for key, dict_ in cfg_rv['dtype'].items()
                if self.file_name in dict_['file']
            }

        sep = ','  # default pandas sep
        if cfg_rv.get('sep'):
            for key, list_ in cfg_rv['sep'].items():
                if self.file_name in list_:
                    sep = key

        encoding = 'utf-8'  # default pandas encoding
        if cfg_rv.get('encoding'):
            for key, list_ in cfg_rv['encoding'].items():
                if self.file_name in list_:
                    encoding = key

        return {'dtype': dtype, 'sep': sep, 'encoding': encoding}

    def save(self, extension):
        """Saves the dataframe on specified path."""
        file_name = Path(self.file_name).with_suffix(extension)
        output_file_path = config.PROCESSED_DIR / file_name
        self.df.to_parquet(output_file_path, compression='gzip')

    # Columns
    def col_add(self, cols: list):
        """Add columns to dataframe with NaN values."""
        for col in cols:
            if col not in self.df.columns:
                self.df[col] = np.nan

    def col_remove(self, cols: list):
        """Removes existing columns from dataframe."""
        filtered_cols = self.df.columns.intersection(pd.Index(cols))
        self.df.drop(filtered_cols, axis=1, inplace=True)

    def col_rename(self, mapping):
        """
        Renames columns according to the provided mapping. See more in:
        https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rename.html
        """
        self.df.rename(mapping, axis='columns', inplace=True)

    def col_reorder(self, cols_in_order: List[str]):
        """
        Reorders columns according to specified order.
        (!) Removes columns not on the list.
        """
        filtered_order = []
        for col in cols_in_order:
            if col in self.df.columns:
                filtered_order.append(col)

        self.df = self.df[filtered_order]

    def col_apply(self, changes: dict):
        """Apply column-related functions based on dictionary."""
        for key, val in changes.items():
            if key == 'remove':
                self.col_remove(val)
            elif key == 'add':
                self.col_add(val)
            elif key == 'rename':
                self.col_rename(val)
            elif key == 'capitalize':
                self.col_rename(str.upper)

    # Values
    def value_impute(self, targets: list) -> None:
        """Replaces NaN values with 0 in specified columns."""
        for column in targets:
            self.df.fillna({column: 0}, inplace=True)

    def value_remove(self, values: dict) -> None:
        """Replaces specified values with NaN in the dataframe."""
        self.df.replace(values, np.nan, inplace=True)

    def value_replace(self, target: dict) -> None:
        """Replaces values according to the provided mapping."""
        self.df.replace(target, inplace=True)

    def value_str_translate(self, target: dict) -> None:
        """Applies string translation to specified columns."""
        for column, value in target.items():
            if isinstance(value, str):
                table = str.maketrans('', '', value)
                self.df[column] = (self.df[column]
                                   .str.translate(table))
            elif isinstance(value, dict):
                for old_value, new_value in value.items():
                    table = str.maketrans(old_value, new_value)
                    self.df[column] = (self.df[column]
                                       .str.translate(table))

    # Dtype
    def dtype_change(self, target: Dict[str, str]) -> None:
        """
        Changes data types of specified columns.
        (!) Auto impute values if dtype is int.
        """
        int_list = [col for col, dtype in target.items()
                    if 'int' in dtype]
        self.value_impute(int_list)

        try:
            self.df = self.df.astype(target)
        except ValueError as ve:
            warn = f'Dtype change not possible: {ve}'
            warnings.warn(warn)
        except TypeError as te:
            warn = f'Incorrect info.: {te}'
            warnings.warn(warn)

    def dtype_optimization(self) -> None:
        """Optimizes numeric data types for memory efficiency."""
        for col in self.df.select_dtypes(include='number').columns:
            if np.issubdtype(self.df[col].dtype, np.integer):
                self.df[col] = pd.to_numeric(self.df[col], downcast='integer')
            elif np.issubdtype(self.df[col].dtype, np.floating):
                self.df[col] = pd.to_numeric(self.df[col], downcast='float')

    def dtype_datetime(self, target: Dict) -> None:
        """
        Converts specified columns to datetime format.
        (!) Invalid dates become pd.NaT.
        """
        for col, format_str in target.items():
            self.df[col] = pd.to_datetime(
                self.df[col], format=format_str, errors='coerce'
            )

            if format_str == '%H%M':
                self.df[col] = self.df[col].dt.time
