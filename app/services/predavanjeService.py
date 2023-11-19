from app.api.dependencies.dependencies import get_db
from app.db.models.predavanje import Predavanje
from app.schemas.predavanjeSchema import PredavanjeBase, PredavanjeInDB
from sqlalchemy.orm import Session
from dotenv import load_dotenv

# from app.schemas.userSchema import User as UserSchema
from fastapi import Depends

load_dotenv()
#potrebno napraviti logiku za predavanja 
def create_predavanje(predavanje: PredavanjeBase, db:Session=Depends(get_db)):
    db_predavanje = Predavanje(
        predavanje.predmet_id,
        predavanje.broj_predavanja
    )
    
    db.add(db_predavanje)
    db.commit()
    db.refresh(db_predavanje)
    
    return PredavanjeInDB(
        db_predavanje.id,
        db_predavanje.predmet_id,
        db_predavanje.broj_predavanja,
        db_predavanje.status,
        db_predavanje.qrcode
    )