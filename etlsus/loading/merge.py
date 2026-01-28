import os
from pathlib import Path

import pyarrow.parquet as pq

from etlsus import config
from etlsus.files import get_files_from_dir


def merger(infix: str) -> Path:
    """
    Concatenates multiple Parquet files into a single file,
    processing row-groups sequentially.
    """
    files = get_files_from_dir(config.PROCESSED_DIR, '.gzip', infix=infix)
    output_path = config.DATA_DIR / f'{infix}.parquet.gzip'

    if output_path.exists():
        return output_path

    main_schema = pq.ParquetFile(files[0]).schema.to_arrow_schema()

    writer = pq.ParquetWriter(output_path, main_schema)

    try:
        for path in files:
            file = pq.ParquetFile(path)
            current_schema = file.schema.to_arrow_schema()

            if not current_schema.equals(main_schema):
                writer.close()
                output_path.unlink()
                raise ValueError(
                    f'Schema of {os.path.basename(path)} does not match the '
                    f'first file.'
                )

            for rg_index in range(file.num_row_groups):
                table = file.read_row_group(rg_index)
                writer.write_table(table)

    finally:
        writer.close()

    return output_path
