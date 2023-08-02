from app.db.connection import Base
from sqlalchemy import Column, INTEGER, func, TEXT, TIMESTAMP, VARCHAR
import shortuuid

class users(Base):
    __tablename__='user_details'
    id = Column(INTEGER, primary_key=True)
    unique_id = Column(VARCHAR(25), default=shortuuid.uuid)
    name = Column(TEXT)
    email = Column(TEXT)
    password = Column(TEXT)
    otp = Column(INTEGER, nullable=True)  
    create_date = Column(TIMESTAMP, default=func.current_timestamp())
    updated_date = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    