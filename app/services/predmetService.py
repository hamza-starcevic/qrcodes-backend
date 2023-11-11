from app.api.dependencies.dependencies import get_db
from sqlalchemy.orm import Session
from app.schemas.predmetSchema import PredmetCreate
from dotenv import load_dotenv

# from app.schemas.userSchema import User as UserSchema
from fastapi import Depends

load_dotenv()
#potrebno napraviti logiku za predavanja 
def create_predmet(predmet: PredmetCreate, db:Session=Depends(get_db)):
    return