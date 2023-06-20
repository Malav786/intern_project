from app.pass_hashing import hasher
from app.models import users, images
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Depends, Header

class login_user():

    def loginuser(db:Session, email: str, password: str):
        user = db.query(users).filter_by(email=email).first()
        if not user or not hasher.verify_pass(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid username or password")
        return user
