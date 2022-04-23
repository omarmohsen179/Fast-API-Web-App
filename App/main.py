
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes.auth import routerauth
from fastapi.testclient import TestClient
from fastapi.staticfiles import StaticFiles
# sqlalchemy uvicorn alembic fastapi pyodbc python-dotenv
# alembic revision --autogenerate -m "create account table"
# alembic upgrade head
# pip freeze > requirements.txt
# Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted powershell
# .\scripts\activate
# python -m pip install --upgrade pip  --force
# uvicorn main:app --reload

app = FastAPI(debug=False)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(routerauth)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.get("/")
def root():
    # return RedirectResponse(url="/docs/")
    return {"running server here we go"}


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
    app.debug = True
    uvicorn.run(app, host="fag1.azurewebsites.net", port=8232)
