import warnings
from pathlib import Path
from typing import Union, List, Dict

import pandas as pd
import numpy as np

import config
from transformation.handlers.utils.time import TimeHandler


class Handler:
    def __init__(self, url: Union[str, Path], **kwargs):
        self.df = pd.read_csv(url, **kwargs)

    def save(self, processed_file_name: str):
        extension = '.parquet.gzip'
        output_path = Path(config.PROCESSED_DIR + processed_file_name
                           + extension).resolve()

        self.df.to_parquet(output_path, compression='gzip')

    # Columns
    def add_cols(self, target: Union[List[str], str]):
        """
        Add cols to dataframe. Values from new columns are filled with np.nan.

        param:
            target List[str] | str: Column(s) to be added
        """
        if type(target) == str:
            self.df[target] = np.nan
        if type(target) == list:
            for i in target:
                self.df[i] = np.nan

    def remove_cols(self, target: Union[List[str], str]):
        """
        Removes target columns from dataframe
        param:
            target List[str] | str: targeted columns to remove
        """
        if type(target) == str:
            target = [target]

        index_ = pd.Index(target)
        filtered_cols = self.df.columns.intersection(index_)

        self.df.drop(filtered_cols, axis=1, inplace=True)

    def rename_cols(self, target_dict: Dict[str, str]):
        """
        Rename columns
        param:
            target_dict Dict[str: str]: old name: new name
        """
        self.df.rename(target_dict, axis=1, inplace=True)

    def organize_cols(self, order: List[str]):
        self.df = self.df[order]

    # Values
    def impute_values(self, target: str):
        self.df.fillna({target: 0}, inplace=True)

    def remove_values(self, values: dict):
        self.df.replace(values, np.nan, inplace=True)

    def replace_values(self, targets: List[Dict]):
        for item in targets:
            self.df.replace(item, inplace=True)

    # Dtype
    def change_dtype(self, target: Dict[str, str]):
        try:
            self.df = self.df.astype(target)
        except ValueError as ve:
            warn = f'Dtype change not possible: {ve}'
            warnings.warn(warn)
        except TypeError as te:
            warn = f'Incorrect info.: {te}'
            warnings.warn(warn)

    def optimize_dtype(self):
        for col in self.df.columns:
            if self.df[col].dtype == np.int64:
                self.df[col] = pd.to_numeric(self.df[col], downcast='integer')
            elif self.df[col].dtype == np.float64:
                self.df[col] = pd.to_numeric(self.df[col], downcast='float')

    def datetime_dtype(self, target: Dict):
        for col, format_str in target.items():
            timeHandler = TimeHandler(format_str)
            self.df[col] = timeHandler.convert_date(self.df[col])

    def combine_date_with_time_dtype(self, target: Dict):
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

