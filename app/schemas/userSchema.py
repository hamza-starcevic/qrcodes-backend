from pydantic import BaseModel, UUID4
from datetime import date


class AccessToken(BaseModel):
    token: str


class UserBase(BaseModel):
    email: str
    firstName: str
    lastName: str
    dateOfBirth: date


class UserCreate(UserBase):
    password: str
    role: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserInDB(UserBase):
    id: UUID4


class UserLoggedIn(UserBase):
    id: UUID4
    token: str
    role: str


class User(UserBase):
    pass
