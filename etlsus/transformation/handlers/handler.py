import warnings
from pathlib import Path
from typing import Union, List, Dict

import pandas as pd
import numpy as np

import config
from .utils.time import TimeHandler


class Handler:
    def __init__(self, url: Union[str, Path], **kwargs):
        self.df = pd.read_csv(url, **kwargs)

    def save(self, processed_file_name: str) -> None:
        """
        Saves the processed dataframe to parquet format with gzip
        compression.

        param:
            processed_file_name (str): Name of the output
                                       file (without extension)
        raises:
            IOError: If file cannot be written to destination
        """
        extension = '.parquet.gzip'
        output_path = Path(str(config.PROCESSED_DIR)
                           + f'/{processed_file_name}{extension}').resolve()

        self.df.to_parquet(output_path, compression='gzip')

    # Columns
    def add_cols(self, target: Union[List[str], str]) -> None:
        """
        Add columns to dataframe with NaN values.

        param:
            target (Union[List[str], str]): Column name(s) to be added
        raises:
            ValueError: If target is not a string or list of strings
        """
        if type(target) is str:
            self.df[target] = np.nan
        if type(target) is list:
            for i in target:
                self.df[i] = np.nan

    def remove_cols(self, target: List[str]) -> None:
        """
        Removes specified columns from dataframe.

        param:
            target (List[str]): List of column names to remove
        raises:
            KeyError: If specified columns don't exist in dataframe
        """
        index_ = pd.Index(target)
        filtered_cols = self.df.columns.intersection(index_)

        self.df.drop(filtered_cols, axis=1, inplace=True)

    def rename_cols(self, target_dict: Dict[str, str]) -> None:
        """
        Renames columns according to the provided mapping.

        param:
            target_dict (Dict[str, str]): Dictionary mapping old
                                          names to new names
        raises:
            KeyError: If old column names don't exist in dataframe
        """
        self.df.rename(target_dict, axis=1, inplace=True)

    def organize_cols(self, order: List[str]) -> None:
        """
        Reorders columns according to specified order.

        param:
            order (List[str]): Desired column order
        raises:
            Warning: If specified columns are missing from dataframe
        """
        filtered_order = []
        missing = []
        for item in order:
            if item in self.df.columns:
                filtered_order.append(item)
            else:
                missing.append(item)

        if missing:
            warnings.warn(f'Missing columns when reordering: {missing}')

        self.df = self.df[filtered_order]

    # Values
    def impute_values(self, targets: list) -> None:
        """
        Replaces NaN values with 0 in specified columns.

        param:
            targets (list): List of column names to impute
        raises:
            KeyError: If specified columns don't exist
        """
        for column in targets:
            self.df.fillna({column: 0}, inplace=True)

    def remove_values(self, values: dict) -> None:
        """
        Replaces specified values with NaN in the dataframe.

        param:
            values (dict): Dictionary mapping values to replace with NaN
        raises:
            TypeError: If values parameter is not a dictionary
        """
        self.df.replace(values, np.nan, inplace=True)

    def replace_values(self, target: dict) -> None:
        """
        Replaces values according to the provided mapping.

        param:
            target (dict): Dictionary mapping old values to new values
        raises:
            TypeError: If target parameter is not a dictionary
        """
        self.df.replace(target, inplace=True)

    # Str specific values
    def translate_str(self, target: dict) -> None:
        """
        Applies string translation to specified columns.

        param:
            target (dict): Dictionary mapping columns to translation rules
        raises:
            AttributeError: If columns don't contain string data
            TypeError: If translation rules are incorrectly formatted
        """
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
    def change_dtype(self, target: Dict[str, str]) -> None:
        """
        Changes data types of specified columns.

        param:
            target (Dict[str, str]): Dictionary mapping columns to
                                     new data types
        raises:
            ValueError: If data type conversion is not possible
            TypeError: If target parameter is incorrectly formatted
            Warning: If conversion fails for some columns
        """
        try:
            self.df = self.df.astype(target)
        except ValueError as ve:
            warn = f'Dtype change not possible: {ve}'
            warnings.warn(warn)
        except TypeError as te:
            warn = f'Incorrect info.: {te}'
            warnings.warn(warn)

    def optimize_dtype(self) -> None:
        """
        Optimizes numeric data types for memory efficiency.

        param:
            None
        raises:
            Warning: If optimization fails for some columns
        """
        for col in self.df.columns:
            if self.df[col].dtype == np.int64:
                self.df[col] = pd.to_numeric(self.df[col], downcast='integer')
            elif self.df[col].dtype == np.float64:
                self.df[col] = pd.to_numeric(self.df[col], downcast='float')

    def datetime_dtype(self, target: Dict) -> None:
        """
        Converts specified columns to datetime format.

        param:
            target (Dict): Dictionary mapping columns to datetime
                           format strings
        raises:
            ValueError: If datetime conversion fails
            Warning: If conversion fails for some values
        """
        for col, format_str in target.items():
            timeHandler = TimeHandler(format_str)
            self.df[col] = timeHandler.convert_date(self.df[col])

    def combine_date_with_time_dtype(self, target: Dict) -> None:
        """
        Combines date and time columns into a single datetime column.

        param:
            target (Dict): Dictionary mapping date column to
                           time column
        raises:
            Warning: If columns are not in datetime format or
                     combination fails
        """
        for date, time in target.items():
            if self.df[date].dtype != '<M8[ns]':
                warn = f'Invalid column selected: {date}'
                warnings.warn(warn)
                return
            elif self.df[time].dtype != '<M8[ns]':
                warn = f'Invalid column selected: {time}'
                warnings.warn(warn)
                return

            zero_hour = pd.to_datetime('0000', format='%M%H')
            self.df[time] = self.df[time].fillna(zero_hour)

            self.df[date] = pd.to_datetime({
                'year'  : self.df[date].dt.year,
                'month' : self.df[date].dt.month,
                'day'   : self.df[date].dt.day,
                'hour'  : self.df[time].dt.hour,
                'minute': self.df[time].dt.minute
            })
