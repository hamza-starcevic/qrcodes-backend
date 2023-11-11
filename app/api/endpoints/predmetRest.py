from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.datastructures import Headers
from sqlalchemy.orm import Session
from app.api.dependencies.dependencies import get_db
from app.schemas.userSchema import User, UserCreate, UserLogin
from app.services.userServices import create_user, login_user, get_users
from app.core.security import check_role

router = APIRouter()

#potrebno napraviti logiku za predavanja 
@router.post("/createPredmet", status_code=status.HTTP_201_CREATED)
def create_predmet():
    return