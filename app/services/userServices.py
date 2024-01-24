from uuid import uuid4
from app.api.dependencies.dependencies import get_db
from sqlalchemy.orm import Session

from app.db.models.predavanje import Predavanje
from app.db.models.predmetKorisnik import PredmetKorisnik
from app.db.models.predavanjeKorisnik import PredavanjeKorisnik
from app.db.models.user import User
from app.schemas.predavanjeKorisnikSchema import PredavanjeKorisnikSaPredmetom
from app.schemas.predmetKorisniciSchema import PredmetKorisnikInDB
from app.schemas.userSchema import User as userSchema
from app.schemas.userSchema import UserCreate, UserLogin, UserLoggedIn
import jwt
import os
from dotenv import load_dotenv

# from app.schemas.userSchema import User as UserSchema
from fastapi import Depends

load_dotenv()


def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        date_of_birth=user.date_of_birth,
        password=user.password,
        role=user.role,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return userSchema(
        id=db_user.id,
        email=db_user.email,
        firstName=db_user.first_name,
        lastName=db_user.last_name,
        dateOfBirth=db_user.date_of_birth,
    )


def login_user(user: UserLogin, db: Session = Depends(get_db)):
    email = user.email
    password = user.password
    db_user = db.query(User).filter(User.email == email).first()
    if db_user.password == password:
        secret = os.getenv("jwt_secret")
        token = jwt.encode(
            {"role": db_user.role}, secret, algorithm="HS256"
        )
        return UserLoggedIn(
            email=db_user.email,
            firstName=db_user.first_name,
            lastName=db_user.last_name,
            datOfBirth=db_user.date_of_birth,
            token=token,
            id=db_user.id
        )
    else:
        return None


def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


def get_users_by_predmet_id(predmet_id: str, db: Session = Depends(get_db)):
    students = db.query(PredmetKorisnik).filter(PredmetKorisnik.predmet_id == predmet_id).all()

    students_list = []
    for student in students:
        students_list.append(
            PredmetKorisnikInDB(
                id=student.id,
                korisnik_id=student.korisnik_id,
                predmet_id=student.predmet_id,
                ime_prezime=student.ime_prezime,
                naziv_predmeta=student.naziv_predmeta,
                role=student.role
            )
        )
    return students_list


def getPrisustvaKorisnika(userId: str, db: Session = Depends(get_db)):
    prisustva = db.query(PredavanjeKorisnik).filter(PredavanjeKorisnik.korisnikId == userId).all()
    zavrsenaPredavanja = []
    for prisustvo in prisustva:
        predmet = db.query(Predavanje).filter(Predavanje.predmet_id == prisustvo.predmet_id)
        zavrsenaPredavanja.append(
            PredavanjeKorisnikSaPredmetom(
                nazivPredmeta=predmet.naziv,
                brojPredavanja=predmet,
                datumPredavanja=prisustvo.datumPredavanja
            )
        )
    return zavrsenaPredavanja
