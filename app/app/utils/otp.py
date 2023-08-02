from app.pass_hashing import hasher
from app.models import users, images
from sqlalchemy.orm import Session
from app.schemas.users import updatePassword
from fastapi import FastAPI, HTTPException, Depends, Header
import random



class login_user():

    def loginuser(db:Session, email: str, password: str):
        user = db.query(users).filter_by(email=email).first()
        if not user or not hasher.verify_pass(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid username or password")
        return user

    @staticmethod
    def generate_otp(email: str, db: Session):
        user = db.query(users).filter_by(email=email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        otp_value = str(random.randint(1000, 9999))
        login_user.update_otp(email, otp_value, db)
        return otp_value

    @staticmethod
    def update_otp(email: str, otp_value: str, db: Session):
        user = db.query(users).filter_by(email=email).first()
        if user:
            user.otp = otp_value
            db.commit()

    @staticmethod
    def verify_otp(sys_otp : int, email: str, otp: int, db: Session) -> bool:
        user = db.query(users).filter_by(email=email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user_otp=int(otp)
        if sys_otp == user_otp:
            user.otp = None
            db.commit()
            return True
        else:
            return False

    @staticmethod
    def update_password(email: str, new_password: str, db: Session):
        user = db.query(users).filter_by(email=email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found") 
        if user:
            hashed_password = hasher.get_pass_hashed(new_password)
            user.password = hashed_password
            db.commit()

    
