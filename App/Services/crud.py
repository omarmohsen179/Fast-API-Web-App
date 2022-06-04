
from requests import Response
from sqlalchemy.orm import Session
from fastapi import status, HTTPException
from fastapi.encoders import jsonable_encoder
from App.models.models import user, role, user_role, item_category
from App.models.schemas import response
from App.Services import base
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union


ModelType = TypeVar("ModelType", bound=base.Base)


class crud(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session):
        return db.query(self.model)

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
            return object
        except BaseException as err:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=Response(success=False, Data=err))

    def add_list(self, db: Session, object):
        try:
            db.add_all(object)
            db.commit()
            # db.refresh(object)
            return object
        except BaseException as err:
            return str(err)

    def update(self, db: Session, object):
        try:
            id = object.Id
            del object.Id
            obj_in_data = jsonable_encoder(object)
            db.query(self.model).filter(
                self.model.Id == id).update(obj_in_data)
            db.commit()
            object.Id = id
            return object
        except BaseException as err:
            return err

    def delete(self, db: Session, id: int):
        db.query(self.model).filter(
            self.model.Id == id).delete()
        db.commit()
        return response(success=True)

    def delete_all(self, db: Session):
        db.query(self.model).delete()
        db.commit()
        return response(success=True)


user_crud = crud(user)
role_crud = crud(role)
categories_crud = crud(item_category)
user_role_crud = crud(user_role)
