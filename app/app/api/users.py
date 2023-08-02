from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session
from app.schemas import users
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.crud import crud_fn
from app.db.connection import get_db

security = HTTPBasic() 

class users():

    router = APIRouter()
    @router.get('/user', response_model=List[users.user])
    def retrieve_all_user_details(credentials: HTTPBasicCredentials = Depends(security),skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        users = crud_fn.get_user(db=db, skip=skip, limit=limit)
        return users


    @router.post('/user', response_model=users.userAdd)
    def add_new_user(user: users.userAdd, db: Session = Depends(get_db)):
        return crud_fn.add_details_to_db(db=db, user=user)


    @router.delete('/user')
    def delete_user_by_id(id: int, credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
        details = crud_fn.get_by_id(db=db, id=id)
        if not details:
            raise HTTPException(status_code=404, detail=f"No record found to delete")

        try:
            crud_fn.delete_details_by_id(db=db, id=id)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Unable to delete: {e}")
        return {"delete status": "success"}


    @router.put('/user', response_model=users.user)
    def update_user_details(user_id: int, update_param: users.updateUser,credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
        details = crud_fn.get_by_id(db=db, id=user_id)
        if not details:
            raise HTTPException(status_code=404, detail=f"No record found to update")
        
        updated_details = crud_fn.update_details(db=db, details=update_param, id=user_id)
        return updated_details
