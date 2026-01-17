from typing import Literal, Union, List

from hydra import compose, initialize

from etlsus import extract, transform, load

def pipeline(
        dataset: Union[Literal['SINASC', 'SIM'], List[str]],
        generic_yaml_file: str,

        file_prefix: str = None,

        table_name: str = None,
        custom_dir: str = None,
        verbose: bool = False,
        **kwargs,
):
    """Main pipeline function"""
    with initialize(version_base=None, config_path='./conf'):
        cfg = compose(config_name='config')

        if dataset == 'SINASC':
            extract(cfg.extract['SINASC'], verbose=verbose)
        elif dataset == 'SIM':
            extract(cfg.extract['SIM'], verbose=verbose)
        else:
            dataset = {
                'prefix': file_prefix,
                'files': dict(zip(range(len(dataset)), dataset))
            }
            extract(dataset, verbose=verbose)

        transform(generic_yaml_file, verbose=verbose)

        if table_name:
            load(table_name, verbose, custom_dir=custom_dir, **kwargs)
