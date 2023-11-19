from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.datastructures import Headers
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from app.schemas.predavanjeSchema import PredavanjeBase
from app.services.predavanjeService import create_predavanje
from app.api.dependencies.dependencies import get_db
from app.core.security import check_role

router = APIRouter()

load_dotenv()
@router.post("/predavanje", status_code=status.HTTP_201_CREATED)
def createPredavanje(predavanje: PredavanjeBase, db:Session=Depends(get_db)):
    predavanjeSaved = create_predavanje(predavanje, db=db)
    return predavanjeSaved