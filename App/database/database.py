import pyodbc
from sqlalchemy import create_engine, MetaData, Column, Integer, String, Boolean, Table
from sqlalchemy.orm import declarative_base, sessionmaker,Session
import urllib
from dotenv import dotenv_values


connection = dotenv_values("pyvenv.cfg")['dbmain']
params = urllib.parse.quote_plus(connection)
pyodbc_connection = pyodbc.connect(connection)
cursor = pyodbc_connection.cursor()
engine = create_engine("mssql+pyodbc:///?odbc_connect={}".format(params), pool_size=10, max_overflow=20, connect_args={"check_same_thread": False})
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=True, autoflush=True, bind=engine)
SessionLocal.begin()
Base.metadata.create_all(engine)




