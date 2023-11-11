from pydantic import BaseModel, UUID4
from datetime import date


class PredmetBase(BaseModel):
    naziv: str
    godina_studija: int

class PredmetCreate(PredmetBase):
    id:UUID4

class Predmet(PredmetBase):
    pass