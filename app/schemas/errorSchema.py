from pydantic import BaseModel


class ErrorBase(BaseModel):
    errorCode: int
    msg: str
