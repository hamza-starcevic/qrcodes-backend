from uuid import uuid4
from app.api.dependencies.dependencies import get_db
from sqlalchemy.orm import Session

from app.db.models.predavanje import Predavanje
from app.db.models.predmet import Predmet
from app.db.models.predmetKorisnik import PredmetKorisnik
from app.db.models.predavanjeKorisnik import PredavanjeKorisnik
from app.db.models.user import User
from app.schemas.predavanjeKorisnikSchema import PredavanjeKorisnikSaPredmetom
from app.schemas.predmetKorisniciSchema import PredmetKorisnikInDB
from app.schemas.predmetSchema import PrisustvaPoPredmetima
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
        first_name=user.firstName,
        last_name=user.lastName,
        date_of_birth=user.dateOfBirth,
        password=user.password,
        role=user.role,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return userSchema(
        id=db_user.id,
        email=db_user.email,
        first_name=db_user.first_name,
        last_name=db_user.last_name,
        date_of_birth=db_user.date_of_birth,
    )


def login_user(user: UserLogin, db: Session = Depends(get_db)):
    print(user)
    email = user.email
    password = user.password
    db_user = db.query(User).filter(User.email == email).first()
    if db_user.password == password:
        secret = os.getenv("jwt_secret")
        print(secret)
        token = jwt.encode(
            {"role": db_user.role}, secret, algorithm="HS256"
        )
        return UserLoggedIn(
            email=db_user.email,
            firstName=db_user.first_name,
            lastName=db_user.last_name,
            dateOfBirth=db_user.date_of_birth,
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
    prisustva = db.query(PredavanjeKorisnik).filter(PredavanjeKorisnik.korisnik_id == userId).all()
    zavrsenaPredavanja = []
    for prisustvo in prisustva:
        predavanje = db.query(Predavanje).filter(Predavanje.id == prisustvo.predavanje_id).first()
        print(predavanje)
        predmet = db.query(Predmet).filter(Predmet.id == predavanje.predmet_id).first()
        zavrsenaPredavanja.append(
            PredavanjeKorisnikSaPredmetom(
                nazivPredmeta=predmet.naziv,
                brojPredavanja=0,
                datumPredavanja=predavanje.datumPredavanja
            )
        )
    return zavrsenaPredavanja


def get_profil_by_korisnik_id(korisnik_id: str, db: Session = Depends(get_db)):
    profil = db.query(User).filter(User.id == korisnik_id).first()

    return profil


def getPrisustvaPoPredmetu(korisnik_id: str, db: Session = Depends(get_db)):
    predmeti = db.query(PredmetKorisnik).filter(PredmetKorisnik.korisnik_id == korisnik_id).all()
    result = []
    for predmet in predmeti:
        predavanja = db.query(Predavanje).filter(Predavanje.predmet_id == predmet.id).all()
        countAll = len(predavanja)
        countPrisutnih = 0
        for predavanje in predavanja:
            if len(db.query(PredavanjeKorisnik).filter(
                    PredavanjeKorisnik.predavanje_id == predavanje.id and PredavanjeKorisnik.korisnik_id == korisnik_id).all()) > 0:
                countPrisutnih += 1
        result.append(
            PrisustvaPoPredmetima(
                nazivPredmeta=predmet.naziv,
                odrzanih=countAll,
                prisutnih=countPrisutnih
            )
        )
    return result

