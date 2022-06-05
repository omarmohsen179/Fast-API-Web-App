
from requests import Response
from sqlalchemy.orm import Session
from fastapi import status, HTTPException
from fastapi.encoders import jsonable_encoder
from App.models.models import user, role, user_role, item_category, item
from App.models.schemas import response
from App.Services import base
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from sqlalchemy.orm import joinedload

ModelType = TypeVar("ModelType", bound=base.Base)


class crud(Generic[ModelType]):
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if crud.__instance == None:
            crud()
        return crud.__instance

    def __init__(self, model: Type[ModelType]):
        crud.__instance = self
        self.model = model

    def get_all(self, db: Session):
        return db.query(self.model).all()

    def get_filter(self, db: Session, filter: Any = None, join: Any = None):
        data = db.query(self.model)
        if join != None:
            for i in join:
                data.options(joinedload(i))
        if filter != None:
            data.filter(filter)
        return data.all()

    def get_pagenation(self, db: Session, skip: int = 0, limit: int = 100):
        return (
            db.query(self.model)
            .order_by(self.model)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def add(self, db: Session, object):
        try:
            del object.Id
            object = self.model(**object.dict())
            db.add(object)
            db.commit()
            db.refresh(object)
            return object
        except BaseException as err:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=Response(success=False, Data=err))

    def add_list(self, db: Session, object):
        try:
            object = list(map(lambda e: self.model(**e.dict()), request))
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


user_crud = crud(user).getInstance()
role_crud = crud(role).getInstance()
categories_crud = crud(item_category).getInstance()
item_crud = crud(item).getInstance()
user_role_crud = crud(user_role).getInstance()
