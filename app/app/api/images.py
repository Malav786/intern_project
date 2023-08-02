from fastapi import  HTTPException, APIRouter
from fastapi import File, UploadFile, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import FileResponse, HTMLResponse
import os
from fastapi import Request
from fastapi.templating import Jinja2Templates
#from pydantic import BaseModel
from app.schemas import images
from app.models import images as image_db
from app.crud import crud_users
from app.db import engine
from app.db.connection import get_db, Base
from app.models import Base, images, users
from typing import List
from app.utils.otp import login_user
from sqlalchemy.orm import Session
from app.utils.token import tokens
from app.crud import crud_fn_imgs, crud_users
from app.api.login import login

IMAGEDIR = "/images"
security = HTTPBasic()
templates = Jinja2Templates(directory="E:/photobooth_Management/app/app/templates") 

class images():

    router = APIRouter()

    @router.get("/user/me")
    def get_current_user(user: dict = Depends(get_db)):
        return user

    @router.post("/upload")
    async def create_upload_file(req: Request, image: UploadFile = File(...), db: Session = Depends(get_db), curruser: str = "malav"):
        name = image.filename
        print(curruser)
        
        #user = login_user.loginuser(db, user)
        if curruser:
            created_by = curruser
            #images.created_by = created_by
            print("ok")
            print(curruser)
            filename = os.path.join("E:/photobooth_Management/app/images", name)  
            #image.filename = f"{uuid.uuid4()}.jpg"
            contents = await image.read()
            with open(f"{filename}", "wb") as f:
                f.write(contents)   
            img = crud_fn_imgs.add_img_details_to_db(db=db, image=filename, created_by="")
            print("HELLLO LOGGING OUT")
            success_message = "Photo uploaded successfully!"
            return templates.TemplateResponse(
                "/landing.html",
                {"request": req, "username": curruser, "success_message": success_message}
            )
            #credentials.username = None
            #credentials.password = None
            #return {"img"};
        else:
            return {"status": "success",
                    "credentials": "FALSE"}
    
    
    @router.get("/show/id")
    def read_imgs_by_id(image_id: int, db: Session = Depends(get_db)):
        image = crud_fn_imgs.get_img_by_id(id=image_id, db=db)
        return image.filename

    @router.get("/show")
    def read_all_imgs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        image = crud_fn_imgs.get_img(db=db, skip=skip, limit=limit)  
        return image
    
    @router.route('/api/images', methods=['GET'])
    def get_image_urls(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        images = crud_fn_imgs.get_img(db=db, skip=skip, limit=limit) 
        image_urls = [image_db.filename for image in images]
        return image_urls

    @router.delete('/image')
    def delete_img_by_id(id: int, db: Session = Depends(get_db)):
        details = crud_fn_imgs.get_img_by_id(db=db, id=id)
        if not details:
            raise HTTPException(status_code=404, detail=f"No record found to delete")

        try:
            crud_fn_imgs.delete_img_details_by_id(db=db, id=id)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Unable to delete: {e}")
        return {"delete status": "success"}

    
    
    
    