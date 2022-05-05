import pyodbc
from sqlalchemy import create_engine, MetaData, Column, Integer, String, Boolean, Table
from sqlalchemy.orm import declarative_base, sessionmaker,Session
import urllib

#from dotenv import dotenv_values


connection = 'Driver={ODBC Driver 17 for SQL Server};Server=tcp:test-server-apps.database.windows.net,1433;Database=ecommercy-web;Uid=admin_omar;Pwd=Asas1212$'

params = urllib.parse.quote_plus(connection)
pyodbc_connection = pyodbc.connect(connection)
cursor = pyodbc_connection.cursor()
engine = create_engine("mssql+pyodbc:///?odbc_connect={}".format(params), pool_size=10, max_overflow=20, connect_args={"check_same_thread": False})
Base = declarative_base()
Base.metadata.create_all(engine)




