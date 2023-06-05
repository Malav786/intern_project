from db.connection import Base
from sqlalchemy import Column, BIGINT, VARCHAR

class student(Base):
    __tablename__='student_details'
    student_id=Column(BIGINT, primary_key=True)
    student_name=Column(VARCHAR(20))
    student_contact=Column(BIGINT)