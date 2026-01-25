from .BaseProcessor import BaseProcessor


class FileProcessor(BaseProcessor):
    def formalize_columns(self, formalize_columns: list, year_specific: dict):
        file_specific = year_specific.get(self.file_name)
        if file_specific:
            self.col_apply(file_specific)

        self.col_add(formalize_columns)
        self.col_reorder(formalize_columns)

    def formalize_values(self, formalize_values):
        self.value_replace(formalize_values)

    def formalize_dtypes(self, formalize_dtype):
        dtype_dict = {
            list_value: key
            for key, value in formalize_dtype.items()
            for list_value in value
        }

        self.dtype_change(dtype_dict)

        self.dtype_optimization()

    def remove_ignored_values(self, ignored_values):
        self.value_remove(ignored_values)

    def fix_dates(self, fix_dates):
        cols = list(fix_dates['columns'].keys())
        str_translate = fix_dates['remove']
        replace = fix_dates['replace']

        self.value_str_translate(str_translate)

        misinput_dict = {col: replace for col in cols}
        self.value_replace(misinput_dict)

        self.dtype_datetime(fix_dates['columns'])

    def pipeline(
            self,
            cfg_trans,
            formalize_columns: bool,
            formalize_values: bool,
            formalize_dtype: bool,
            remove_ignored_values: bool,
            fix_dates: bool,
    ):
        if formalize_columns:
            self.formalize_columns(
                cfg_trans['formalize_columns'],
                cfg_trans['year_specific'],
            )

        if formalize_values:
            self.formalize_values(cfg_trans['formalize_values'])

        if formalize_dtype:
            self.formalize_dtypes(cfg_trans['formalize_dtypes'])

        if remove_ignored_values:
            self.remove_ignored_values(cfg_trans['ignored_values'])

        if fix_dates:
            self.fix_dates(cfg_trans['fix_dates'])
