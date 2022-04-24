from sqlalchemy import create_engine, MetaData, Column, Integer, String, Boolean, Table
from sqlalchemy.orm import declarative_base, sessionmaker
#from dotenv import dotenv_values
import urllib

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
    "mssql+pyodbc://omar:Mrj8P8kSSUGDqNRP1e@subue1.database.windows.net:1433/FastApi2?driver=SQL+Server"
    # "jdbc:sqlserver://subue1.database.windows.net:1433;database=FastApi2;user=omar@subue1;password=Mrj8P8kSSUGDqNRP1e;encrypt=true;trustServerCertificate=false;hostNameInCertificate=*.database.windows.net;loginTimeout=30;"
)
SessionLocal = sessionmaker(bind=engine)
metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
