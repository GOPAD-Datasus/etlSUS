import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def create_base_dir() -> Path:
    if 'base_dir' in os.environ:
        return Path(os.environ['base_dir']).resolve()
    else:
        try:
            return Path(__file__).resolve().parent
        except NameError:
            return Path.cwd().resolve()


BASE_DIR = create_base_dir()
DATA_DIR = BASE_DIR / 'data'
RAW_DIR = DATA_DIR / 'raw'
PROCESSED_DIR = DATA_DIR / 'processed'

RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def get_database_config(env='prod'):
    if env == 'test':
        return {'USER':     'test_user',
                'PASSWORD': '***',
                'HOST':     'localhost',
                'PORT':     '12345',
                'DB':       'test_db'}
    else:
        required = ['user', 'password', 'host', 'port', 'db']
        if any(os.getenv(var) is None for var in required):
            raise EnvironmentError("Incomplete .env file")

        return {'USER': os.environ['user'],
                'PASSWORD': os.environ['password'],
                'HOST': os.environ['host'],
                'PORT': os.environ['port'],
                'DB': os.environ['db']}
