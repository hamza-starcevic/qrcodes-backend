from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.datastructures import Headers
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from app.schemas.predavanjeKorisnikSchema import PredavanjeKorisnik

from app.schemas.predavanjeSchema import PredavanjeBase
from app.services.predavanjeService import add_user_predavanje, create_predavanje, generate_qrcode, get_all_predavanja, get_predavanje_by_id
from app.api.dependencies.dependencies import get_db
from app.core.security import check_role

router = APIRouter(tags=["Predavanja"])

load_dotenv()

@router.post("/create", status_code=status.HTTP_201_CREATED)
def createPredavanje(predavanje: PredavanjeBase, db: Session = Depends(get_db)):
    """
    Create a new Predavanje record in the database.

    Args:
        predavanje (PredavanjeBase): The Predavanje data to be saved.
        db (Session, optional): The database session dependency. Defaults to Depends(get_db).

    Returns:
        PredavanjeInDB: The created Predavanje record, including its ID and any other auto-generated fields.
    """
    predavanjeSaved = create_predavanje(predavanje, db=db)
    return predavanjeSaved

@router.post("/{predavanje_id}/generate/qrcode")
def generateQRCode(predavanje_id: str, db: Session = Depends(get_db)):
    """
    Generate a QR code for a specific Predavanje identified by its ID.

    Args:
        predavanje_id (str): The ID of the Predavanje for which to generate the QR code.
        db (Session, optional): The database session dependency. Defaults to Depends(get_db).

    Returns:
        Response: A response indicating the success of the QR code generation.
    """
    return generate_qrcode(predavanje_id=predavanje_id, db=db)

@router.get("/all")
def getAllPredavanja(db: Session = Depends(get_db)):
    """
    Retrieve all Predavanje records from the database.

    Args:
        db (Session, optional): The database session dependency. Defaults to Depends(get_db).

    Returns:
        List[PredavanjeInDB]: A list of all Predavanje records in the database.
    """
    return get_all_predavanja(db=db)

@router.get("/{predavanje_id}")
def getPredavanjeById(predavanje_id: str, db: Session = Depends(get_db)):
    """
    Retrieve a specific Predavanje by its ID.

    Args:
        predavanje_id (str): The ID of the Predavanje to retrieve.
        db (Session, optional): The database session dependency. Defaults to Depends(get_db).

    Returns:
        PredavanjeInDB: The requested Predavanje record.
    """
    return get_predavanje_by_id(predavanje_id=predavanje_id, db=db)

@router.post("/korisnik")
def addKorisnikToPredavanje(content: PredavanjeKorisnik, db: Session = Depends(get_db)):
    return add_user_predavanje(content=content, db=db)