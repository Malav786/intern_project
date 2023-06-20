from sqlalchemy.orm import Session
import app.models
from app.schemas.schema import userAdd, updateUser
from app.pass_hashing import hasher
from app.models import users


class crud_fn():
    

    def get_by_id( db: Session, id: int):
        return db.query(app.models.users).filter(app.models.users.id == id).first()


    def get_by_id( db: Session, id: int):
        return db.query(app.models.users).filter(app.models.users.id == id).first()


    def get_user( db: Session, skip: int = 0, limit: int = 100):
        return db.query(app.models.users).offset(skip).limit(limit).all()


    def add_details_to_db( db: Session, user: userAdd):
        mv_details = app.models.users(
            name=user.name,
            email=user.email,
            password=hasher.get_pass_hashed(user.password)
        )
        db.add(mv_details)
        db.commit()
        db.refresh(mv_details)
        return app.models.users(**user.dict())
        


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
