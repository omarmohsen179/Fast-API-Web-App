
from fastapi.staticfiles import StaticFiles
from fastapi.testclient import TestClient
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from App.schemas import *
from fastapi.middleware.gzip import GZipMiddleware

from App.Routes import auth, item, role
# sqlalchemy uvicorn alembic fastapi pyodbc python-dotenv
# alembic revision --autogenerate -m "create account table"
# alembic upgrade head
# pip freeze > requirements.txt
# Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted powershell
# .\scripts\activate
# python -m pip install --upgrade pip  --force
# uvicorn App.main:app --reload
# git push --force azurex
# git fetch --all
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.add_middleware(GZipMiddleware)
app.include_router(auth.router)
app.include_router(item.router)
app.include_router(role.router)


@app.get("/db")
def root():
    # return RedirectResponse(url="/docs/")
    return {"running server here we go 8x"}


@app.get("/")
def root():
    # return RedirectResponse(url="/docs/")
    return {"running server here we go 8x"}


client = TestClient(app)


def initial_data():
    response = client.post(
        "/role/list",
        json=[{"Id": 1, "Name": "User"},
              {"Id": 2, "Name": "Admin"}
              ],
    )
    # print(response)
    #assert response.status_code == 200, response.text


# initial_data()
if __name__ == "__main__":
    app.debug = False
    uvicorn.run(app, host="fag1.azurewebsites.net", port=443)
