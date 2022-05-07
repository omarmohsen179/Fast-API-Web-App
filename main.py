
from fastapi.staticfiles import StaticFiles
from fastapi.testclient import TestClient
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from App.schemas import *
from fastapi.middleware.gzip import GZipMiddleware
from App.middlewares.validation_middleware import FieldValidation
from App.middlewares.db_middleware import DBConnection
from App.middlewares.db_exceptions import DBException
from App.Routes import auth, service, role
# sqlalchemy uvicorn alembic fastapi pyodbc python-dotenv
# alembic revision --autogenerate -m "create account table"
# alembic upgrade head
# pip freeze > requirements.txt
# Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted powershell
# .\scripts\activate
# python -m pip install --upgrade pip  --force
# python -m ensurepip pip not found
# uvicorn main:app --reload
# git push --force azurex
# git remote add azure "https://omarmohsen179@ecommercy.scm.azurewebsites.net/ecommercy.git"
# git fetch --all
app = FastAPI(debug=True)
app.mount("/static", StaticFiles(directory="static"), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
app.add_middleware(DBConnection)
app.add_middleware(DBException)
app.add_middleware(FieldValidation)
app.add_middleware(GZipMiddleware)
app.include_router(auth.router)
app.include_router(service.router)
app.include_router(role.router)


@app.get("/")
def root():
    # return RedirectResponse(url="/docs/")
    return {"running server here we go 4"}

if __name__ == "__main__":
    app.debug = False
    uvicorn.run(app, host="fag1.azurewebsites.net", port=443)
