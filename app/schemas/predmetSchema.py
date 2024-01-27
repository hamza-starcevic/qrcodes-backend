from pydantic import BaseModel, UUID4
from datetime import date


class PredmetBase(BaseModel):
    naziv: str
    godina_studija: int


class PredmetInDB(PredmetBase):
    id: UUID4


class PrisustvaPoPredmetima(BaseModel):
    nazivPredmeta: str
    odrzanih: int
    prisutnih: int


class Predmet(PredmetBase):
    pass
