import datetime

from app.api.dependencies.dependencies import get_db
from app.db.models.predavanje import Predavanje
from app.db.models.predavanjeKorisnik import PredavanjeKorisnik as PredavanjeKorisnikModel
from app.schemas.predavanjeKorisnikSchema import PredavanjeKorisnik, PredavanjeKorisnikInDB
from app.schemas.predavanjeSchema import PredavanjeBase, PredavanjeInDB
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from io import BytesIO

import qrcode as qr
import base64

# from app.schemas.userSchema import User as UserSchema
from fastapi import Depends, HTTPException

load_dotenv()
#potrebno napraviti logiku za predavanja 
def create_predavanje(predavanje: PredavanjeBase, db:Session=Depends(get_db)) -> PredavanjeInDB:
    db_predavanje = Predavanje(
        predmet_id = predavanje.predmet_id,
        broj_predavanja = predavanje.broj_predavanja,
        datum_predavanja = datetime.datetime.now(),
        qrcode = "To be generated"
    )
    
    db.add(db_predavanje)
    db.commit()
    db.refresh(db_predavanje)
    
    return PredavanjeInDB(
        id = db_predavanje.id,
        predmet_id = db_predavanje.predmet_id,
        broj_predavanja = db_predavanje.broj_predavanja,
        status = db_predavanje.status,
        qrcode = "To be generated"
    )

def generate_qrcode(predavanje_id: str, db: Session = Depends(get_db)) -> PredavanjeInDB:
    img = qr.make(predavanje_id)
    buffered = BytesIO()
    img.save(buffered)
    img_base64 = base64.b64encode(buffered.getvalue()).decode()

    # Update the database record with the base64 string
    db_predavanje = db.query(Predavanje).filter(Predavanje.id == predavanje_id).first()
    if db_predavanje:
        db_predavanje.qrcode = img_base64
        db.commit()
        return PredavanjeInDB(
        id = db_predavanje.id,
        predmet_id = db_predavanje.predmet_id,
        broj_predavanja = db_predavanje.broj_predavanja,
        status = db_predavanje.status,
        qrcode = db_predavanje.qrcode
        )
    


def get_predavanje_by_id(predavanje_id: int, db: Session = Depends(get_db)) -> PredavanjeInDB:
    # Query the database for the predavanje with the given ID
    db_predavanje = db.query(Predavanje).filter(Predavanje.id == predavanje_id).first()

    # If no predavanje is found, raise an HTTPException
    if db_predavanje is None:
        raise HTTPException(status_code=404, detail="Predavanje not found")

    # Convert the database model instance to a Pydantic model
    return PredavanjeInDB(
        id = db_predavanje.id,
        predmet_id = db_predavanje.predmet_id,
        broj_predavanja = db_predavanje.broj_predavanja,
        status = db_predavanje.status,
        qrcode = db_predavanje.qrcode
    )

def get_all_predavanja(db: Session = Depends(get_db)) -> list[PredavanjeInDB]:
    # Query the database for all predavanja
    db_predavanja = db.query(Predavanje).all()

    # Convert each database model instance to a Pydantic model
    return [PredavanjeInDB(
        id = predavanje.id,
        predmet_id = predavanje.predmet_id,
        broj_predavanja = predavanje.broj_predavanja,
        status = predavanje.status,
        qrcode = predavanje.qrcode
    ) for predavanje in db_predavanja]

def add_user_predavanje(content: PredavanjeKorisnik ,db: Session = Depends(get_db)) -> PredavanjeKorisnik:
    db_result = PredavanjeKorisnikModel(
        predavanjeId = content.predavanje_id,
        korisnikId = content.korisnik_id,
        imePrezime = content.ime_prezime,
        nazivPredavanja = content.naziv_predavanja
    )
    
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    
    return PredavanjeKorisnikInDB(
        id=db_result.id,
        predavanjeId=db_result.predavanje_id,
        korisnikId=db_result.korisnik_id,
        imePrezime=db_result.ime_prezime,
        nazivPredavanja=db_result.naziv_predavanja
    )