import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Determine DB Path based on environment
if os.environ.get("VERCEL"):
    db_path = "/tmp/sklad.db"
else:
    db_path = "./sklad.db"

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{db_path}")

# Use check_same_thread only for SQLite
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
