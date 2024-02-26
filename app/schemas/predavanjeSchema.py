from typing import Optional
from pydantic import BaseModel, UUID4
from datetime import date


class PredavanjeBase(BaseModel):
    predmet_id: UUID4
    broj_predavanja: int
    datumPredavanja: Optional[date] = None
    status: str


class PredavanjeInDB(PredavanjeBase):
    id: UUID4
    datumPredavanja: date
    qrcode: str


class Predavanje(PredavanjeBase):
    pass
