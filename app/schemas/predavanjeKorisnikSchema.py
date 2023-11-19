from pydantic import BaseModel, UUID4

class PredavanjeKorisnikBase(BaseModel):
    predavanje_id:UUID4
    korisnik_id:UUID4
    ime_prezime: str
    naziv_predavanja: str

class PredavanjeKorisnikInDB(PredavanjeKorisnikBase):
    id:UUID4

class PredavanjeKorisnik(PredavanjeKorisnikBase):
    pass