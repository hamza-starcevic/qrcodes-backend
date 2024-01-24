from pydantic import BaseModel, UUID4

class PredmetKorisnikBase(BaseModel):
    predmetId:UUID4
    korisnikId:UUID4
    imePrezime: str
    nazivPredmeta: str
    role: str

class PredmetKorisnikInDB(PredmetKorisnikBase):
    id:UUID4

class PredmetKorisnik(PredmetKorisnikBase):
    pass