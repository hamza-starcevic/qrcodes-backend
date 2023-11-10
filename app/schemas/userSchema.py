from pydantic import BaseModel, UUID4
from datetime import date


class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str
    date_of_birth: date

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserInDB(UserBase):
    id: UUID4
    hashed_password: str

class User(UserBase):
    pass