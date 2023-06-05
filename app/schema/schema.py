from pydantic import BaseModel
from fastapi import FastAPI

class register(BaseModel):
    id: int
    name: str 
    email: str
    password: str
    confirm_password: str