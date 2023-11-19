from pydantic import BaseModel, UUID4

class PredmetKorisnikBase(BaseModel):
    predmet_id:UUID4
    korisnik_id:UUID4
    ime_prezime: str
    naziv_predmeta: str
    role: str

class PredmetKorisnikInDB(PredmetKorisnikBase):
    id:UUID4

class PredmetKorisnik(PredmetKorisnikBase):
    pass