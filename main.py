
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from App.Routes import auth, item, role
from fastapi.testclient import TestClient
# sqlalchemy uvicorn alembic fastapi pyodbc
# alembic revision --autogenerate -m "create account table"
# alembic upgrade head
# pip freeze > requirements.txt
#uvicorn main:app --reload
#Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted powershell
# .\scripts\activate        
# python -m pip install --upgrade pip  --force
#.\scripts\activate.bat
app = FastAPI()

app.include_router(auth.router)
app.include_router(item.router)
app.include_router(role.router)
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
    return {"running server"}


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
    uvicorn.run(app, host="localhost", port=8001)
