import pyodbc
from sqlalchemy import create_engine, MetaData, Column, Integer, String, Boolean, Table
from sqlalchemy.orm import declarative_base, sessionmaker
import urllib
#from dotenv import dotenv_values
Base = declarative_base()
metadata = MetaData()

notes = Table(
    "notes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("text", String),
    Column("completed", Boolean),
)

connection = 'Driver={ODBC Driver 17 for SQL Server};Server=tcp:test-server-apps.database.windows.net,1433;Database=ecommercy-web;Uid=admin_omar;Pwd=Asas1212$'

params = urllib.parse.quote_plus(connection)
pyodbc_connection = pyodbc.connect(connection)
cursor = pyodbc_connection.cursor()
engine = create_engine("mssql+pyodbc:///?odbc_connect={}".format(params))
SessionLocal = sessionmaker(bind=engine)
metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
