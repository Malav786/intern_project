from app.db.connection import Base
from sqlalchemy import Column, INTEGER, TEXT, TIMESTAMP, func, VARCHAR, ForeignKey
from app.models import users
import shortuuid


class images(Base):
    __tablename__='images'
    id=Column(INTEGER, primary_key=True)
    unique_id=Column(VARCHAR(25), default=shortuuid.uuid)
    filename=Column(TEXT)
    create_time=Column(TIMESTAMP, default=func.current_timestamp())
    updated_date = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    created_by = Column(TEXT)