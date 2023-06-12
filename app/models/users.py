from app.db.connection import Base
from sqlalchemy import Column, INTEGER, VARCHAR, TEXT

class users(Base):
    __tablename__='user_details'
    user_id=Column(INTEGER, primary_key=True)
    user_name=Column(TEXT)
    user_email=Column(TEXT)
    user_password=Column(TEXT)
    user_conf_password=Column(TEXT)