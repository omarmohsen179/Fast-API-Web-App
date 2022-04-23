from sqlalchemy import create_engine, MetaData, Column, Integer, String, Boolean, Table
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import dotenv_values


Base = declarative_base()
metadata = MetaData()

notes = Table(
    "notes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("text", String),
    Column("completed", Boolean),
)
engine = create_engine(
    "mssql://omar:Om123456@92.204.138.94:53956/Fast_Api_Test?driver=SQL+Server"
    # "server=92.204.138.94\\MD_MEDAD_WEB; database=Fast_Api_Test; User id=omar;password =Om123456; Trusted_Connection=True;Integrated Security=false;", pool_size=3, max_overflow=0
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
