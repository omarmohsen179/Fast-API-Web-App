
from sqlalchemy.orm import Session
from fastapi import status, HTTPException
from fastapi.encoders import jsonable_encoder
from App.schemas import Response


class crud:

    def get_filter(self, db: Session, condition):
        return db.query(self.model).filter(condition)

    def get_pagenation(self, db: Session, skip: int = 0, limit: int = 100):
        return (
            db.query(self.model)
            .order_by(self.model)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_all(self, db: Session):
        return db.query(self.model).all()

    def add(self, db: Session, object):
        try:
            db.add(object)
            db.commit()
            db.refresh(object)
            return Response(success=True, Data=object)
        except BaseException as err:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=Response(success=False, Data=err))

    def update(self, db: Session, object):
        id = object.Id
        del object.Id
        obj_in_data = jsonable_encoder(object)
        try:
            db.query(self.model).filter(
                self.model.Id == id).update(obj_in_data, synchronize_session="fetch")
            db.commit()
            return Response(success=True, Data=object)
        except BaseException as err:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=Response(success=False, Data=err))

    def delete(self, db: Session, id: int):
        db.query(self.model).filter(
            self.model.Id == id).delete()
        db.commit()
        return Response(success=True)
