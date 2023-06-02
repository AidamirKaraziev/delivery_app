from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from src.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
metadata = MetaData()
Base = declarative_base(metadata=metadata)

engine = create_engine(DATABASE_URL)
Session = sessionmaker(engine)


def get_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()
