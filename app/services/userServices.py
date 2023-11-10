from app.api.dependencies.dependencies import get_db
from sqlalchemy.orm import Session
from app.db.models.user import User
from app.schemas.userSchema import UserCreate, UserLogin
from app.schemas.userSchema import User as UserSchema
from app.core.security import get_password_hash, verify_password
from fastapi import Depends

def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)

    db_user = User(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        date_of_birth=user.date_of_birth,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return UserSchema(
        id=db_user.id,
        email=db_user.email,
        first_name=db_user.first_name,
        last_name=db_user.last_name,
        date_of_birth=db_user.date_of_birth
    )

def login_user(user:UserLogin, db: Session = Depends(get_db)):
    email = user.email
    password = user.password
    db_user = db.query(User).filter(User.email == email).first()
    if verify_password(password, db_user.hashed_password):
        return UserSchema(
            id=db_user.id,
            email=db_user.email,
            first_name=db_user.first_name,
            last_name=db_user.last_name,
            date_of_birth=db_user.date_of_birth
        )
    else:
        return None