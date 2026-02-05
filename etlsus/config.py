import os
import tempfile
from pathlib import Path


def create_data_dir() -> Path:
    path = os.environ.get('ETLSUS_DATA_DIR', tempfile.gettempdir())
    return Path(path).resolve()


DATA_DIR = create_data_dir()
RAW_DIR = DATA_DIR / 'raw'
PROCESSED_DIR = DATA_DIR / 'processed'

RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
