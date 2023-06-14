from pydantic import BaseModel, validator


class imgBase(BaseModel):
    image_id: int
    image_filename: str



class imgAdd(BaseModel):
    image_filename: str


class image(imgAdd):
    class Config:
        orm_mode = True


class imgProduct(BaseModel):
    image_id: int
    image_filename: str

    class Config:
        orm_mode = True

class updateimg(BaseModel):
    image_id: int
    image_filename: str

    class Config:
        orm_mode = True
