import os
import atexit

from sqlalchemy import ForeignKey, Integer, String, Text, create_engine, Column, DateTime, func
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'password')
POSTGRES_USER = os.getenv('POSTGRES_USER', 'user')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'lecture')
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
    header = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    owner = Column(String, ForeignKey('user.name', ondelete='CASCADE'), nullable=False)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    registration_time = Column(DateTime, server_default=func.now())

    @property
    def dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'registrated_at': self.registration_time
        }


Base.metadata.create_all(engine)
