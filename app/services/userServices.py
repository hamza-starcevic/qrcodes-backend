from app.api.dependencies.dependencies import get_db
from sqlalchemy.orm import Session
from app.db.models.user import User
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
        first_name=db_user.first_name,
        last_name=db_user.last_name,
        date_of_birth=db_user.date_of_birth,
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
            first_name=db_user.first_name,
            last_name=db_user.last_name,
            date_of_birth=db_user.date_of_birth,
            token=token,
        )
    else:
        return None

def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users