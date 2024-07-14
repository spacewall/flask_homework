import os
import atexit

from sqlalchemy import create_engine

POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'password')
POSTGRES_USER = os.getenv('POSTGRES_USER', 'user')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'lecture')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', '127.0.0.1')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5431')

PG_DSN = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

engine = create_engine(PG_DSN)

atexit.register(engine.dispose)
