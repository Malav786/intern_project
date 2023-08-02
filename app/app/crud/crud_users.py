from sqlalchemy.orm import Session
from fastapi import Request
import app.models
from app.schemas.users import userAdd, updateUser
from app.pass_hashing import hasher
from app.models import users
from fastapi import HTTPException
from fastapi import APIRouter, HTTPException, Response
from app.db.connection import get_db
from fastapi import Depends, Form
from app.utils.token import tokens
from fastapi import HTTPException, status
import jwt

secret_key = 'asdf'
algorithm = 'HS256'

class crud_fn():
    

    def get_by_id( db: Session, id: int):
        return db.query(app.models.users).filter(app.models.users.id == id).first()

    def get_by_username( db: Session, email: str):
        return db.query(app.models.users).filter(app.models.users.email == email).first()

    def get_user( db: Session, skip: int = 0, limit: int = 100):
        return db.query(app.models.users).offset(skip).limit(limit).all()


    def add_details_to_db(db: Session, user: userAdd):
        existing_user = db.query(app.models.users).filter_by(email=user.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already exists")

        mv_details = app.models.users(
            name=user.name,
            email=user.email,
            password=hasher.get_pass_hashed(user.password)
        )
        db.add(mv_details)
        db.commit()
        db.refresh(mv_details)
        return True
        #return app.models.users(**user.dict())
    


    def update_details( db: Session, id: int, details: updateUser):
        updated_values = {
        users.name: details.name,
        users.email: details.email
    }
        db.query(app.models.users).filter(app.models.users.id == id).update(updated_values)
        db.commit()
        return db.query(app.models.users).filter(app.models.users.id == id).first()


    def delete_details_by_id( db: Session, id: int):
        try:
            db.query(app.models.users).filter(app.models.users.id == id).delete()
            db.commit()
        except Exception as e:
            raise Exception(e)
        
    
    def get_current_user(request: Request, response:Response, db:Session=Depends(get_db), username : str = Form(...), password:str=Form(...)):
        # Here, you would perform your authentication logic
        # This is just a simple example to illustrate the usage

        token = tokens.create_token(username, db)
        # Perform authentication logic based on the token

        # If authentication fails, raise an exception
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        payload = jwt.decode(token, key = secret_key, algorithms = algorithm)
        user = payload.get('user')
        print(user)
        return username
