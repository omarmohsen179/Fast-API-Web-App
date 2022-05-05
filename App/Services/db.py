
from App.models import Session,engine
def db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()