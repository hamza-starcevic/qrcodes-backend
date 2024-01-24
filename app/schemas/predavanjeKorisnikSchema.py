from datetime import datetime

from pydantic import BaseModel, UUID4

class PredavanjeKorisnikBase(BaseModel):
    predavanjeId:UUID4
    korisnikId:UUID4
    imePrezime: str
    nazivPredavanja: str

class PredavanjeKorisnikSaPredmetom(BaseModel):
    nazivPredmeta: str
    brojPredavanja: int
    datumPredavanja: datetime

class PredavanjeKorisnikInDB(PredavanjeKorisnikBase):
    id:UUID4

class PredavanjeKorisnik(PredavanjeKorisnikBase):
    pass