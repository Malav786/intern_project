from fastapi import Depends, FastAPI, HTTPException
from fastapi import FastAPI, File, UploadFile
import os
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.schemas import schema_img
from app.db import engine
import uuid
from app.db.connection import get_db, Base
from app.models import users, Base, images
from typing import List
from sqlalchemy.orm import Session
from app.crud import crud_fn, crud_fn_imgs
from app.schemas import schema
from random import randint

from tkinter import Tk
from tkinter.filedialog import askopenfilenames

Base.metadata.create_all(bind=engine)
IMAGEDIR = "images/"

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


@app.post("/upload/")
def create_upload_file(image: UploadFile = File(...), db: Session = Depends(get_db)):    
    return crud_fn_imgs.add_img_details_to_db(db=db, image=image)
 
 
@app.get("/show/id")
def read_imgs_by_id(image_id: int, db: Session = Depends(get_db)):
    image = db.query(images).get(image_id)   
    return image

@app.get("/show")
def read_all_imgs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    image = crud_fn_imgs.get_img(db=db, skip=skip, limit=limit)   
    return image

@app.delete('/image')
def delete_img_by_id(id: int, db: Session = Depends(get_db)):
    details = crud_fn_imgs.get_img_by_id(db=db, id=id)
    if not details:
        raise HTTPException(status_code=404, detail=f"No record found to delete")

    try:
        crud_fn_imgs.delete_img_details_by_id(db=db, id=id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unable to delete: {e}")
    return {"delete status": "success"}