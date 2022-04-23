
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


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


if __name__ == "__main__":
    uvicorn.run(app, host="fag1.azurewebsites.net", port=8232)
