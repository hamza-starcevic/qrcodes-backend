from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.dependencies.dependencies import get_db
from app.schemas.userSchema import User, UserCreate, UserLogin
from app.services.userServices import create_user, login_user

router = APIRouter()

@router.post("/register", response_model=User, status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(user = user, db=db)

@router.post("/login", response_model=User, status_code=200)
def login(user: UserLogin, db: Session = Depends(get_db)):
    return login_user(user = user, db=db)
