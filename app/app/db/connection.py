from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import Form
from fastapi.security import HTTPBasic, HTTPBasicCredentials

# db_uri='postgresql://127.0.0.1/student_db?user=postgres&password=malav'
db_uri='postgresql://postgres:malav@localhost:5432/photobooth_db'

engine=create_engine(
    db_uri, connect_args={}, future=True
)

sessionlocal=sessionmaker(
    autocommit=False, autoflush=False, bind=engine, future=True
)

Base=declarative_base()
security = HTTPBasic() 

def get_db():
    db=sessionlocal()
    try:
        yield db
    finally:
        db.close()



