from pydantic import BaseModel, EmailStr, validator


class userBase(BaseModel):
    name: str
    email: EmailStr
    password: str



class userAdd(userBase):
    class Config:
        orm_mode = True


class user(userAdd):
    class Config:
        orm_mode = True


class userProduct(BaseModel):
    name : str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True

class updateUser(BaseModel):
    name: str
    email: EmailStr

    class Config:
        orm_mode = True

class updatePassword(BaseModel):
    otp: int
    new_password: str

    class Config:
        orm_mode = True




