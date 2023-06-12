from sqlalchemy.orm import Session
import app.models
from app.schemas.schema import userAdd, updateUser
from app.pass_hashing import hasher


class crud_fn():
    

    def get_user_by_user_id( db: Session, user_id: int):
        return db.query(app.models.users).filter(app.models.users.user_id == user_id).first()


    def get_user_by_id( db: Session, id: int):
        return db.query(app.models.users).filter(app.models.users.user_id == id).first()


    def get_user( db: Session, skip: int = 0, limit: int = 100):
        return db.query(app.models.users).offset(skip).limit(limit).all()


    def add_user_details_to_db( db: Session, user: userAdd):
        mv_details = app.models.users(
    
            user_name=user.user_name,
            user_email=user.user_email,
            user_password=hasher.get_pass_hashed(user.user_password)
        )
        db.add(mv_details)
        db.commit()
        db.refresh(mv_details)
        return app.models.users(**user.dict())
        


    def update_user_details( db: Session, user_id: int, details: updateUser):
        db.query(app.models.users).filter(app.models.users.user_id == user_id).update(vars(details))
        db.commit()
        return db.query(app.models.users).filter(app.models.users.user_id == user_id).update()


    def delete_user_details_by_id( db: Session, id: int):
        try:
            db.query(app.models.users).filter(app.models.users.user_id == id).delete()
            db.commit()
        except Exception as e:
            raise Exception(e)
