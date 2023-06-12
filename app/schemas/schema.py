from pydantic import BaseModel, EmailStr, validator


class userBase(BaseModel):
    user_id: int
    user_name: str
    user_email: EmailStr
    user_password: str



class userAdd(userBase):
    class Config:
        orm_mode = True


class user(userAdd):
    class Config:
        orm_mode = True


class userProduct(BaseModel):
    user_id: int
    user_name : str
    user_email: EmailStr
    user_password: str

    class Config:
        orm_mode = True

class updateUser(BaseModel):
    user_id: int
    user_name: str
    user_email: EmailStr
    user_password: str

    class Config:
        orm_mode = True
