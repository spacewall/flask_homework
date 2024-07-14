import os
import atexit

import dotenv
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Integer, String, Text, create_engine, DateTime, func, Column

CONFIGURATION = dotenv.dotenv_values('.env')

POSTGRES_PASSWORD = CONFIGURATION['POSTGRES_PASSWORD']
POSTGRES_USER = CONFIGURATION['POSTGRES_USER']
POSTGRES_DB = CONFIGURATION['POSTGRES_DB']
POSTGRES_HOST = os.getenv('POSTGRES_HOST', '127.0.0.1')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5431')

PG_DSN = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

engine = create_engine(PG_DSN)

atexit.register(engine.dispose)

Session = sessionmaker(engine)

Base = declarative_base()

 
class Advertisement(Base):
    __tablename__ = 'ads'

    id = Column(Integer, primary_key=True)
    header = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

    @property
    def dict(self) -> dict:
        return {
            'id': self.id,
            'header': self.header,
            'description': self.description,
            'created_at': self.created_at.isoformat()
        }


Base.metadata.create_all(engine)
