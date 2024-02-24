import time
from uuid import uuid4

import bcrypt
from pydantic import InstanceOf
from sqlalchemy.exc import IntegrityError
from app.api.dependencies.dependencies import get_db
from sqlalchemy.orm import Session

from app.db.models.predavanje_model import Predavanje
from app.db.models.predmet_model import Predmet
from app.db.models.predmetKorisnik_model import PredmetKorisnik
from app.db.models.predavanjeKorisnik_model import PredavanjeKorisnik
from app.db.models.user_model import User
from app.exceptions.customExceptions import (
    HAAAMUserAlreadyExists,
    HAAAMUserDoesNotExist,
)
from app.schemas.errorSchema import ErrorBase
from app.schemas.predavanjeKorisnikSchema import PredavanjeKorisnikSaPredmetom
from app.schemas.predmetKorisniciSchema import PredmetKorisnikInDB
from app.schemas.predmetSchema import PrisustvaPoPredmetima
from app.schemas.userSchema import AccessToken, User as userSchema
from app.schemas.userSchema import UserCreate, UserLogin, UserLoggedIn
import jwt
import os
from dotenv import load_dotenv

# from app.schemas.userSchema import User as UserSchema
from fastapi import Depends

from app.schemas.utilSchema import StatusOk

load_dotenv()


def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = db.query(User).filter(User.email == user.email).first()
        if db_user:
            raise HAAAMUserAlreadyExists("User already exists")
        hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())

        db_user = User(
            email=user.email,
            first_name=user.firstName,
            last_name=user.lastName,
            date_of_birth=user.dateOfBirth,
            password=hashed_password.decode("utf-8"),
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
    except HAAAMUserAlreadyExists as e:
        return ErrorBase(errorCode=400, msg=e.msg)
    except Exception as e:
        print(e)
        return ErrorBase(errorCode=500, msg="Error creating user")


def login_user(user: UserLogin, db: Session = Depends(get_db)):
    try:
        email = user.email
        db_user = db.query(User).filter(User.email == email).first()
        if db_user == None:
            raise HAAAMUserDoesNotExist("User does not exist")
        decrypted_password = bcrypt.checkpw(
            user.password.encode("utf-8"), db_user.password.encode("utf-8")
        )
        if decrypted_password == False:
            raise HAAAMUserDoesNotExist("Invalid credentials")

        token = jwt.encode(
            {"role": db_user.role, "exp": time.time() + 86400},
            os.getenv("jwt_secret"),
            algorithm="HS256",
        )
        return UserLoggedIn(
            email=db_user.email,
            firstName=db_user.first_name,
            lastName=db_user.last_name,
            dateOfBirth=db_user.date_of_birth,
            token=token,
            id=db_user.id,
        )
    except HAAAMUserDoesNotExist as e:
        return ErrorBase(errorCode=400, msg=e.msg)
    except Exception as e:
        print(e)
        return ErrorBase(errorCode=500, msg="Error logging in user")


def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


def get_users_by_predmet_id(predmet_id: str, db: Session = Depends(get_db)):
    try:
        students = (
            db.query(PredmetKorisnik)
            .filter(PredmetKorisnik.predmet_id == predmet_id)
            .all()
        )

        students_list = []
        for student in students:
            students_list.append(
                PredmetKorisnikInDB(
                    id=student.id,
                    korisnik_id=student.korisnik_id,
                    predmet_id=student.predmet_id,
                    ime_prezime=student.ime_prezime,
                    naziv_predmeta=student.naziv_predmeta,
                    role=student.role,
                )
            )
        return students_list
    except Exception as e:
        print(e)
        return ErrorBase(errorCode=500, msg="Error getting users by predmet id")


def getPrisustvaKorisnika(userId: str, db: Session = Depends(get_db)):
    try:
        prisustva = (
            db.query(PredavanjeKorisnik)
            .filter(PredavanjeKorisnik.korisnik_id == userId)
            .all()
        )
        zavrsenaPredavanja = []
        for prisustvo in prisustva:
            predavanje = (
                db.query(Predavanje)
                .filter(Predavanje.id == prisustvo.predavanje_id)
                .first()
            )
            print(predavanje)
            predmet = (
                db.query(Predmet).filter(Predmet.id == predavanje.predmet_id).first()
            )
            zavrsenaPredavanja.append(
                PredavanjeKorisnikSaPredmetom(
                    nazivPredmeta=predmet.naziv,
                    brojPredavanja=0,
                    datumPredavanja=predavanje.datumPredavanja,
                )
            )
        return zavrsenaPredavanja
    except Exception as e:
        print(e)
        return ErrorBase(
            errorCode=500, msg="Nije moguce dobiti prisustva korisnika po predmetu"
        )


def get_profil_by_korisnik_id(korisnik_id: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == korisnik_id).first()

    return UserLoggedIn(
        email=db_user.email,
        firstName=db_user.first_name,
        lastName=db_user.last_name,
        dateOfBirth=db_user.date_of_birth,
        token="",
        id=db_user.id,
    )


def getPrisustvaPoPredmetu(korisnik_id: str, db: Session = Depends(get_db)):
    try:
        predmeti = (
            db.query(PredmetKorisnik)
            .filter(PredmetKorisnik.korisnik_id == korisnik_id)
            .all()
        )
        result = []
        for predmet in predmeti:
            print(predmet.id)
            predavanja = (
                db.query(Predavanje)
                .filter(Predavanje.predmet_id == predmet.predmet_id)
                .all()
            )
            countAll = len(predavanja)
            countPrisutnih = 0
            for predavanje in predavanja:
                if (
                    len(
                        db.query(PredavanjeKorisnik)
                        .filter(
                            PredavanjeKorisnik.predavanje_id == predavanje.id
                            and PredavanjeKorisnik.korisnik_id == korisnik_id
                        )
                        .all()
                    )
                    > 0
                ):
                    countPrisutnih += 1
            result.append(
                PrisustvaPoPredmetima(
                    nazivPredmeta=predmet.naziv_predmeta,
                    odrzanih=countAll,
                    prisutnih=countPrisutnih,
                )
            )
        return result
    except Exception as e:
        print(e)
        return ErrorBase(errorCode=500, msg="Nije moguce dobiti prisustva po predmetu")


def validateJwtToken(token: str, db: Session = Depends(get_db)):
    try:
        decoded = jwt.decode(token, os.getenv("jwt_secret"), algorithms=["HS256"])
        return AccessToken(token=token)
    except jwt.ExpiredSignatureError as e:
        return ErrorBase(errorCode=401, msg="Token expired")
    except Exception as e:
        print(e)
        return ErrorBase(errorCode=401, msg="Invalid token")


def delete_user(id: str, db: Session = Depends(get_db)):
    try:
        db_user = db.query(User).filter(User.id == id).delete()
        if db_user == None:
            raise HAAAMUserDoesNotExist("User does not exist")
        db.commit()
        return StatusOk(status="User deleted")
    except HAAAMUserDoesNotExist as e:
        return ErrorBase(errorCode=400, msg=e.msg)
    except IntegrityError as e:
        return ErrorBase(
            errorCode=400,
            msg="Brisanje nije uspjelo: Korisnik je dodijeljen na jedan od predmeta!",
        )
    except Exception as e:
        print(type(e))
        return ErrorBase(errorCode=500, msg=e)


def get_users_by_role(role: str, db: Session = Depends(get_db)):
    try:
        users = db.query(User).filter(User.role == role).all()

        if users == None:
            return []
        result = []
        for user in users:
            result.append(
                userSchema(
                    id=user.id,
                    email=user.email,
                    firstName=user.first_name,
                    lastName=user.last_name,
                    dateOfBirth=user.date_of_birth,
                )
            )
    except Exception as e:
        print(e)
        return ErrorBase(
            errorCode=500, msg="Desio se problem prilikom dohvatanja korisnika po roli"
        )
