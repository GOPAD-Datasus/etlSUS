import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

if 'base_dir' in os.environ:
    BASE_DIR = Path(os.environ['base_dir']).resolve()
else:
    try:
        BASE_DIR = Path(__file__).resolve().parent
    except NameError:
        BASE_DIR = Path.cwd().resolve()

DATA_DIR = BASE_DIR / 'data'
RAW_DIR = DATA_DIR / 'raw'
PROCESSED_DIR = DATA_DIR / 'processed'

RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
