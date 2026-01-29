import os
from pathlib import Path


def create_base_dir() -> Path:
    path = os.environ.get('ETLSUS_BASE_DIR')
    return Path(path).resolve()


BASE_DIR = create_base_dir()
DATA_DIR = BASE_DIR / 'data'
RAW_DIR = DATA_DIR / 'raw'
PROCESSED_DIR = DATA_DIR / 'processed'

RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
