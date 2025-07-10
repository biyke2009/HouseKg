from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from sqlalchemy.ext.declarative import declarative_base
from fastapi import FastAPI

DATABASE_URL='postgresql://postgres:admin@localhost:5432/House_app'

Base = declarative_base()

engine = create_engine(DATABASE_URL)

SessionLocale = sessionmaker(bind=engine)


