from uuid import uuid4
from app.api.dependencies.dependencies import get_db
from sqlalchemy.orm import Session
from app.db.models.predmetKorisnik import PredmetKorisnik
from app.db.models.user import User
from app.schemas.predmetKorisniciSchema import PredmetKorisnikInDB
from app.schemas.userSchema import User as userSchema
from app.schemas.userSchema import UserCreate, UserLogin, UserLoggedIn
import jwt, os
from dotenv import load_dotenv

# from app.schemas.userSchema import User as UserSchema
from fastapi import Depends

load_dotenv()


def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(
        email=user.email,
        firstName=user.firstName,
        lastName=user.lastName,
        dateOfBirth=user.dateOfBirth,
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
        )
    else:
        return None

def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

def get_users_by_predmet_id(predmet_id: str,db: Session = Depends(get_db)):
    students = db.query(PredmetKorisnik).filter(PredmetKorisnik.predmet_id==predmet_id).all()

    students_list =[]
    for student in students:
        students_list.append(
            PredmetKorisnikInDB(
                id = student.id,
                korisnikId=student.korisnik_id,
                predmetId=student.predmet_id,
                imePrezime=student.ime_prezime,
                nazivPredmeta=student.naziv_predmeta,
                role=student.role
            )
        )
    return students_list