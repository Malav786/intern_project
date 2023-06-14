from app.db.connection import Base
from sqlalchemy import Column, INTEGER, TEXT

class images(Base):
    __tablename__='images'
    image_id=Column(INTEGER, primary_key=True)
    image_filename=Column(TEXT)