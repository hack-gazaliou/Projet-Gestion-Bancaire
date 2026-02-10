"""
Create the engine and the session of sqlalchemy
for communicating with the database.
Create the database if not present.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///bank.db"

engine = create_engine(DATABASE_URL)
SESSIONLOCAL = sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base()
