from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.engine import URL

from dotenv import dotenv_values
import main
engine = create_engine(
    dotenv_values("pyvenv.cfg")['Db']
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False,)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
