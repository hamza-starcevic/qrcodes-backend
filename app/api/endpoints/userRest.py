from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.datastructures import Headers
from sqlalchemy.orm import Session
from app.api.dependencies.dependencies import get_db
from app.schemas.errorSchema import ErrorBase
from app.schemas.userSchema import User, UserCreate, UserLoggedIn, UserLogin
from app.services.userServices import (
    create_user,
    get_profil_by_korisnik_id,
    get_users_by_predmet_id,
    login_user,
    get_users,
    getPrisustvaKorisnika,
    getPrisustvaPoPredmetu,
)
from app.core.security import check_role

router = APIRouter(tags=["Users"])


@router.post("/create", status_code=status.HTTP_201_CREATED)
def createUser(user: UserCreate, request: Request, db: Session = Depends(get_db)):
    # if not check_role(headers=request.headers, roleToBe="admin"):
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Unauthorized",
    #     )
    return handleResponse(create_user(user=user, db=db))


@router.post("/login", status_code=status.HTTP_200_OK)
def login(user: UserLogin, db: Session = Depends(get_db)):
    return handleResponse(login_user(user=user, db=db))


@router.get("/{token}", status_code=200)
def getUsers(token: str, db: Session = Depends(get_db)):
    # if not check_role({"Authorization":token}, roleToBe="admin"):
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Unauthorized",
    #     )
    users = get_users(db=db)
    return users


@router.get("/predmet/{predmet_id}")
def getUsersByPredmetId(predmet_id: str, db: Session = Depends(get_db)):
    return handleResponse(get_users_by_predmet_id(predmet_id=predmet_id, db=db))


@router.get("/profil/{korisnik_id}")
def getUserProfile(korisnik_id: str, db: Session = Depends(get_db)):
    profil = get_profil_by_korisnik_id(korisnik_id=korisnik_id, db=db)

    return profil


@router.get("/predavanja/{korisnik_id}")
def getUserProfile(korisnik_id: str, db: Session = Depends(get_db)):
    return handleResponse(getPrisustvaKorisnika(korisnik_id=korisnik_id, db=db))


@router.get("/predavanja/predmet/{korisnik_id}")
def getUserProfile(korisnik_id: str, db: Session = Depends(get_db)):
    return handleResponse(getPrisustvaPoPredmetu(korisnik_id=korisnik_id, db=db))


def handleResponse(result):
    if isinstance(result, ErrorBase) != True:
        return result
    else:
        raise HTTPException(
            status_code=result.errorCode,
            detail=result.msg,
        )
