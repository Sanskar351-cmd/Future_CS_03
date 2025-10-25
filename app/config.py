import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = BASE_DIR / 'storage'
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

class Config:
    SECRET_KEY = os.environ.get('FLASK_SECRET', 'dev-secret')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(BASE_DIR / 'storage' / 'files.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MASTER_PASSPHRASE = os.environ.get('MASTER_PASSPHRASE')  # required
    KDF_ITERATIONS = int(os.environ.get('KDF_ITERATIONS', 200_000))
    SALT_PATH = str(STORAGE_DIR / 'salt.bin')
    STORAGE_DIR = str(STORAGE_DIR)
