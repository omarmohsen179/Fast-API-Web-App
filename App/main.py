from dotenv import load_dotenv
import uvicorn
from fastapi import FastAPI
import os
from App.Routes import auth
from dotenv import dotenv_values
app = FastAPI()
# sqlalchemy uvicorn alembic fastapi pyodbc
# alembic revision --autogenerate -m "create account table"
#
app.include_router(auth.router)


load_dotenv()

GCP_PROJECT_ID = os.getenv('GCP_PROJECT_ID')
SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE')
STORAGE_BUCKET_NAME = os.getenv('STORAGE_BUCKET_NAME')
print(dotenv_values(".env"))


@app.get("/")
def root():
    return os.getenv("SERVICE_ACCOUNT_FILE")


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001)
