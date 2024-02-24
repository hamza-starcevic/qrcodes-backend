from pydantic import BaseModel


class StatusOk(BaseModel):
    status: str
