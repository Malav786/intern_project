from sqlalchemy.orm import Session
import app.models
from app.schemas import imgAdd, updateimg

from fastapi import Depends, FastAPI, HTTPException
from fastapi import FastAPI, File, UploadFile
import uuid
from app.db.connection import get_db, Base
from app.models import users, Base, images
from typing import List
from sqlalchemy.orm import Session
import uuid
from app.schemas import schema_img


IMAGEDIR = "app/images/"
class crud_fn_imgs():
    

    def get_img_by_img_id( db: Session, image_id: int):
        return db.query(app.models.images).filter(app.models.images.image_id == image_id).first()


    def get_img_by_id( db: Session, id: int):
        return db.query(app.models.images).filter(app.models.images.image_id == id).first()


    def get_img( db: Session, skip: int = 0, limit: int = 100):
        return db.query(app.models.images).offset(skip).limit(limit).all()


    def add_img_details_to_db(db:Session, image: imgAdd):
            image_data = image.file.read()
            db_image = images(image_filename=image.filename)
            db.add(db_image)
            db.commit()
            db.refresh(db_image)
            return {"message": "Image created successfully"}
        


    def update_img_details( db: Session, image_id: int, details: updateimg):
        db.query(app.models.all_images).filter(images.image_id == image_id).update(vars(details))
        db.commit()
        return db.query(app.models.all_images).filter(images.image_id == image_id).update()


    def delete_img_details_by_id( db: Session, id: int):
        try:
            db.query(app.models.images).filter(images.image_id == id).delete()
            db.commit()
        except Exception as e:
            raise Exception(e)
