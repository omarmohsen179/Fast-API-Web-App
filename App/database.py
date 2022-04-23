from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import dotenv_values

engine = create_engine(
    'mssql+pyodbc://omar:Om123456@92.204.138.94:53956/Fast_Api_Test?driver=SQL+Server'
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False,)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
