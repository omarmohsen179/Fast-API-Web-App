
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from App.Routes import auth, item
from fastapi.testclient import TestClient
app = FastAPI()
# sqlalchemy uvicorn alembic fastapi pyodbc
# alembic revision --autogenerate -m "create account table"
# pip freeze > requirements.txt
app.include_router(auth.router)
app.include_router(item.router)

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


client = TestClient(main.app)


def insial_data():
    response = client.post(
        "/role",
        json={"Name": "User"},
    )
    assert response.status_code == 200, response.text


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001)
