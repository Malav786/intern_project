import jwt
from datetime import datetime, timedelta
from app.models import users
from app.db.connection import get_db
from fastapi import Depends
from sqlalchemy.orm import Session

secret_key = 'asdf'
algorithm = 'HS256'

class tokens():
    def create_token(email: str, db: Session = Depends(get_db)):
        user = db.query(users).filter_by(email=email).first()
        payload = {
            'user_id': user.id,
            'username': email,
            'exp': datetime.utcnow() + timedelta(hours=1)  
        }
        
        token = jwt.encode(payload, secret_key, algorithm)
        return token

    def verify_token(token):
        try:
            payload = jwt.decode(token, key = secret_key, algorithms = algorithm)
            return payload
        except Exception as ex:
            raise ex