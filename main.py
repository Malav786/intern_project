from fastapi import Depends, FastAPI, HTTPException
from fastapi import FastAPI, File, UploadFile, BackgroundTasks, status, Body, Depends, Header
from fastapi.security import HTTPBasic, HTTPBasicCredentials

#from fastapi.responses import FileResponse
import os
from pydantic import BaseModel
from app.schemas import schema_img
from app.db import engine
from app.db.connection import get_db, Base
from app.models import users, Base, images
from typing import List
from app.login_system import login
from sqlalchemy.orm import Session
from app.crud import crud_fn, crud_fn_imgs
from app.schemas import schema
from app.mediapipe import image_classify
from subprocess import Popen

Base.metadata.create_all(bind=engine)
IMAGEDIR = "/images"
security = HTTPBasic() 

app = FastAPI()

@app.get('/user', response_model=List[schema.user])
def retrieve_all_user_details(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud_fn.get_user(db=db, skip=skip, limit=limit)
    return users


@app.post('/user', response_model=schema.userAdd)
def add_new_user(user: schema.userAdd, db: Session = Depends(get_db)):
    return crud_fn.add_details_to_db(db=db, user=user)


@app.delete('/user')
def delete_user_by_id(id: int, db: Session = Depends(get_db)):
    details = crud_fn.get_by_id(db=db, id=id)
    if not details:
        raise HTTPException(status_code=404, detail=f"No record found to delete")

    try:
        crud_fn.delete_details_by_id(db=db, id=id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unable to delete: {e}")
    return {"delete status": "success"}


@app.put('/user', response_model=schema.user)
def update_user_details(user_id: int, update_param: schema.updateUser, db: Session = Depends(get_db)):
    details = crud_fn.get_by_id(db=db, id=user_id)
    if not details:
        raise HTTPException(status_code=404, detail=f"No record found to update")
    
    updated_details = crud_fn.update_details(db=db, details=update_param, id=user_id)
    return updated_details





@app.post("/upload/")
async def create_upload_file(created_by: str, image: UploadFile = File(...), db: Session = Depends(get_db)):
    name = image.filename
    images.created_by = created_by
    filename = os.path.join("E:/photobooth_Management/app/images", name)  
    #image.filename = f"{uuid.uuid4()}.jpg"
    contents = await image.read()
    with open(f"{filename}", "wb") as f:
        f.write(contents)   
    return crud_fn_imgs.add_img_details_to_db(db=db, image=filename, created_by=created_by)
 
 
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

def run_streamlit():
    st_process=Popen(["Streamlit", "run", "E:/photobooth_Management/app/app/mediapipe/classification.py"])

@app.get('/classify')
def classify_img(bg_task: BackgroundTasks):
    bg_task.add_task(run_streamlit)
    return "Done"


@app.get('/login')
def user_login(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db),):
    user = login.login_user.loginuser(db, credentials.username, credentials.password)
    return {"message": "Logged in successfully"}