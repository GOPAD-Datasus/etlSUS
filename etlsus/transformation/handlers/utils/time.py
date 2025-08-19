import pandas as pd


class TimeHandler:
    def __init__(self, format_str: str = None):
        self.format = format_str

    def _get_format_item_length(self) -> int:
        length = 0
        format_directives = {
            'Y': 4,  # Year with century
            'y': 2,  # Year without century
            'm': 2,  # Month
            'd': 2,  # Day
            'H': 2,  # Hour (24-hour)
            'I': 2,  # Hour (12-hour)
            'M': 2,  # Minute
            'S': 2,  # Second
            'f': 6,  # Microsecond
            'j': 3,  # Day of year
            'W': 2,  # Week number
            'U': 2,  # Week number (Sunday)
            'w': 1,  # Weekday
            'V': 2,  # ISO week number
            'X': 8,  # Time representation
            'x': 8,  # Date representation

            '%': 0
        }

        for i in range(len(self.format)):
            length += format_directives.get(self.format[i], 1)

        return length

    def _correct_length(self, date_str: str):
        format_length = self._get_format_item_length()
        if len(date_str) == format_length:
            return date_str
        elif len(date_str) > format_length:
            return date_str[:format_length]
        else:
            return pd.NaT

    def convert_date(self, series: pd.Series):
        """
        Standardizes columns related to dates and time by
        converting to datetime.
        """
        return pd.to_datetime(series.apply(self._correct_length),
                              format=self.format,
                              errors='coerce')
