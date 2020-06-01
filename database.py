from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
#import psycopg2
#sqlite3 stocks.db
#.schema stocks

SQLALCHEMY_DATABASE_URL = "sqlite:///./stocks.db"
#SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Nbareddit@12@localhost:5433/stockDatabase"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()