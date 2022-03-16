from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.engine import URL

'''connection_string = "DRIVER={SQL Server Native Client 10.0};SERVER=92.204.138.94\\MD_MEDAD_WEB;DATABASE=Fast_Api_Test;UID=khalid;PWD=Y@$$er@2020"
connection_url = URL.create(
    "mssql+pyodbc", query={"odbc_connect": connection_string})
     "mssql+pyodbc://admin1:admin1@localhost/suapp52?driver=SQL+Server"
    '''

engine = create_engine(
    "mssql+pyodbc://omar:Om123456@92.204.138.94:53956/Fast_Api_Test?driver=SQL+Server"
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False,)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
