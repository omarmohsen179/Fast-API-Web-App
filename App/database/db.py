
from App.models.models import Session,engine,SessionLocal,session
def db2():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
def db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()