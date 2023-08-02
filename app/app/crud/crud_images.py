import app.models
from app.schemas import imgAdd, updateimg

from fastapi import Depends, FastAPI, HTTPException
from fastapi import FastAPI, File, UploadFile

from app.db.connection import get_db, Base
from app.models import users, Base, images
from typing import List
from sqlalchemy.orm import Session
from app.schemas import images as image_schema


IMAGEDIR = "app/images/"
class crud_fn_imgs():
    

    def get_img_by_img_id( db: Session, image_id: int):
        return db.query(app.models.images).filter(app.models.images.id == image_id).first()


    def get_img_by_id( db: Session, id: int):
        return db.query(app.models.images).filter(app.models.images.id == id).first()


    def get_img( db: Session, skip: int = 0, limit: int = 100):
        return db.query(app.models.images).offset(skip).limit(limit).all()


    def add_img_details_to_db(db:Session, image: imgAdd, created_by):
            #image_data = image.file.read()
            db_image = images(filename=image, created_by=created_by)
            db.add(db_image)
            db.commit()
            db.refresh(db_image)
            return {"status": "success",
                    "message": "Image created successfully"}
    
    def delete_img_details_by_id( db: Session, id: int):
        try:
            db.query(app.models.images).filter(images.id == id).delete()
            db.commit()
        except Exception as e:
            raise Exception(e)
        
    def get_image_urls_from_database(db: Session) -> List[str]:
        # Assuming you have a model named Image that represents the images table in the database
        # Replace 'Image' with your actual model name
        

        # Fetch the image URLs from the database using the provided session
        image_db = db.query(images).all()
        
        # Extract the image URLs from the retrieved Image objects
        image_urls = [image.url for image in image_db]

        return image_urls
