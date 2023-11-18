from app.api.dependencies.dependencies import get_db
from sqlalchemy.orm import Session
from app.db.models.predmet import Predmet
from app.db.models.predmetKorisnik import PredmetKorisnik
from app.schemas.predmetKorisniciSchema import PredmetKorisnik as PK, PredmetKorisnikInDB
from app.schemas.predmetSchema import PredmetBase, PredmetInDB
from dotenv import load_dotenv

# from app.schemas.userSchema import User as UserSchema
from fastapi import Depends

load_dotenv()
#potrebno napraviti logiku za predavanja 
def create_predmet(predmet: PredmetBase, db:Session=Depends(get_db)):
    db_predmet = Predmet(
        naziv = predmet.naziv,
        godina_studija = predmet.godina_studija
    )

    db.add(db_predmet)
    db.commit()
    db.refresh(db_predmet)
    
    predmetCreated = PredmetInDB(
        id =  db_predmet.id,
        naziv = db_predmet.naziv,
        godina_studija= db_predmet.godina_studija
    )
    
    return predmetCreated

def get_predmeti(db:Session = Depends(get_db)):
    predmeti = db.query(Predmet).all()
    predmetList = []
    for predmet in predmeti:
        predmetList.append(
            PredmetInDB(
                id = predmet.id,
                naziv = predmet.naziv,
                godina_studija = predmet.godina_studija
            )
        )
    return predmetList

def add_korisnik(content: PK, db:Session = Depends(get_db)):
    db_result = PredmetKorisnik(
        korisnik_id = content.korisnik_id,
        predmet_id = content.predmet_id,
        naziv_predmeta =content.naziv_predmeta,
        ime_prezime = content.ime_prezime,
        role = content.role
    )
    db.add(db_result)
    db.commit()
    db.refresh(db_result)

    return PredmetKorisnikInDB(
        id = db_result.id,
        korisnik_id = db_result.korisnik_id,
        predmet_id = db_result.predmet_id,
        naziv_predmeta = db_result.naziv_predmeta,
        ime_prezime = db_result.ime_prezime,
        role = db_result.role
    )
