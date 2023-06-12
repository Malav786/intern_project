from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
#import app.schemas
from app.db import engine
from app.db.connection import get_db, Base
from app.models import users, Base
from typing import List
from sqlalchemy.orm import Session
from app.crud import crud_fn 

from app.schemas import schema

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get('/user', response_model=List[schema.user])
def retrieve_all_user_details(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud_fn.get_user(db=db, skip=skip, limit=limit)
    return users


@app.post('/user', response_model=schema.userAdd)
def add_new_user(user: schema.userAdd, db: Session = Depends(get_db)):
    return crud_fn.add_user_details_to_db(db=db, user=user)


@app.delete('/user')
def delete_user_by_id(id: int, db: Session = Depends(get_db)):
    details = crud_fn.get_user_by_id(db=db, id=id)
    if not details:
        raise HTTPException(status_code=404, detail=f"No record found to delete")

    try:
        crud_fn.delete_user_details_by_id(db=db, id=id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unable to delete: {e}")
    return {"delete status": "success"}


@app.put('/user', response_model=schema.user)
def update_user_details(user_id: int, update_param: schema.updateUser, db: Session = Depends(get_db)):
    details = crud_fn.get_user_by_id(db=db, id=user_id)
    if not details:
        raise HTTPException(status_code=404, detail=f"No record found to update")
    return crud_fn.update_user_details(db=db, details=update_param, id=id)