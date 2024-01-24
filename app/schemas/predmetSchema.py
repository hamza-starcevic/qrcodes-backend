from pydantic import BaseModel, UUID4
from datetime import date


class PredmetBase(BaseModel):
    naziv: str

class PredmetInDB(PredmetBase):
    id:UUID4

class Predmet(PredmetBase):
    pass


