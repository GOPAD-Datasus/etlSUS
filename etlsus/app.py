from etlsus import extract, transform, load


def pipeline(
        input_file_url: str,
        generic_yaml_file: str = None,
        table_name: str = None,
        custom_dir: str = None,
        verbose: bool = False,
        **kwargs,
):
    """Main pipeline function"""
    extract(input_file_url, verbose=verbose)

    transform(generic_yaml_file, verbose=verbose)

    if table_name:
        load(table_name, verbose, custom_dir=custom_dir, **kwargs)
