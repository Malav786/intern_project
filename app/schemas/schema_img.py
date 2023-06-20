from pydantic import BaseModel, validator


class imgBase(BaseModel):
    id: int
    filename: str



class imgAdd(BaseModel):
    filename: str


class image(imgAdd):
    class Config:
        orm_mode = True


class imgProduct(BaseModel):
    id: int
    filename: str

    class Config:
        orm_mode = True

class updateimg(BaseModel):
    filename: str

    class Config:
        orm_mode = True
