from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.datastructures import Headers
from sqlalchemy.orm import Session
from app.api.dependencies.dependencies import get_db
from app.api.endpoints.userRest import handleResponse
from app.schemas.predmetKorisniciSchema import PredmetKorisnik
from app.schemas.predmetSchema import PredmetBase
from app.services.predmetService import add_korisnik, create_predmet, get_predmeti
from app.core.security import check_role

router = APIRouter(tags=["Predmeti"])


# potrebno napraviti logiku za predavanja
@router.post("/create", status_code=status.HTTP_201_CREATED)
def createPredmet(
    predmet: PredmetBase, request: Request, db: Session = Depends(get_db)
):
    return create_predmet(predmet=predmet, db=db)


@router.get("/all", status_code=status.HTTP_200_OK)
def getPredmeti(db: Session = Depends(get_db)):
    return handleResponse(get_predmeti(db=db))


@router.post("/korisnik", status_code=status.HTTP_200_OK)
def addKorisnik(content: PredmetKorisnik, db: Session = Depends(get_db)):
    return add_korisnik(content=content, db=db)
