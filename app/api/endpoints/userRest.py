from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.datastructures import Headers
from sqlalchemy.orm import Session
from app.api.dependencies.dependencies import get_db
from app.schemas.userSchema import User, UserCreate, UserLogin
from app.services.userServices import create_user, login_user, get_users
from app.core.security import check_role

router = APIRouter()


@router.post("/createUser", status_code=201)
def createUser(user: UserCreate,request: Request, db: Session = Depends(get_db)):
    if not check_role(headers=request.headers, roleToBe="admin"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )
    newUser = create_user(user=user, db=db)
    if newUser == None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error creating user",
        )
    return newUser

@router.post(
    "/login",
    status_code=200,
)
def login(user: UserLogin, db: Session = Depends(get_db)):
    loggedUser = login_user(user=user, db=db)
    if user == None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )
    else:
        return loggedUser
    
@router.get("/users", status_code=200)
def getUsers(headers = Headers, db: Session = Depends(get_db)):
    if not check_role(headers=headers, roleToBe="admin"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )
    users = get_users(db=db)
    return users
