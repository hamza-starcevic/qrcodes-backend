from app.api.dependencies.dependencies import get_db
from sqlalchemy.orm import Session
from app.db.models.predmet_model import Predmet
from app.db.models.predmetKorisnik_model import PredmetKorisnik
from app.exceptions.customExceptions import HAAMGenericError
from app.schemas import utilSchema
from app.schemas.errorSchema import ErrorBase
from app.schemas.predmetKorisniciSchema import PredmetKorisnikCreateDTO
from app.schemas.predmetSchema import PredmetBase, PredmetInDB, PredmetSaProfesorom
from dotenv import load_dotenv

# from app.schemas.userSchema import User as UserSchema
from fastapi import Depends

from app.db.models.user_model import User as UserDB

load_dotenv()


# potrebno napraviti logiku za predavanja
def create_predmet(predmet: PredmetBase, db: Session = Depends(get_db)):
    db_predmet = Predmet(naziv=predmet.naziv, godina_studija=predmet.godinaStudija)

    db.add(db_predmet)
    db.commit()
    db.refresh(db_predmet)

    predmetCreated = PredmetInDB(
        id=db_predmet.id,
        naziv=db_predmet.naziv,
        godinaStudija=db_predmet.godina_studija,
    )

    return predmetCreated


def get_predmeti(db: Session = Depends(get_db)):
    try:
        predmeti = db.query(Predmet).all()
        if not predmeti:
            return []
        predmetList = []
        for predmet in predmeti:
            profesori_na_predmetu = (
                db.query(PredmetKorisnik)
                .filter(
                    PredmetKorisnik.predmet_id == predmet.id,
                    PredmetKorisnik.role == "profesor",
                )
                .all()
            )
            lista_profesora = ""
            for profesor in profesori_na_predmetu:
                lista_profesora += profesor.ime_prezime + ", "
            if lista_profesora != "":
                lista_profesora = lista_profesora[:-2]
            predmetList.append(
                PredmetSaProfesorom(
                    id=predmet.id,
                    naziv=predmet.naziv,
                    godinaStudija=predmet.godina_studija,
                    profesor=lista_profesora,
                )
            )
        return predmetList
    except Exception as e:
        print(e)
        return ErrorBase(errorCode=500, msg="Error fetching predmeti")


def add_korisnik(content: PredmetKorisnikCreateDTO, db: Session = Depends(get_db)):
    try:
        user = db.query(UserDB).filter(UserDB.id == content.korisnikId).first()
        if not user:
            raise HAAMGenericError("Korisnik ne postoji")
        predmet = db.query(Predmet).filter(Predmet.id == content.predmetId).first()
        if not predmet:
            raise HAAMGenericError("Predmet ne postoji")
        db_result = PredmetKorisnik(
            korisnik_id=content.korisnikId,
            predmet_id=content.predmetId,
            naziv_predmeta=predmet.naziv,
            ime_prezime=user.first_name + " " + user.last_name,
            role=user.role,
        )
        db.add(db_result)
        db.commit()
        db.refresh(db_result)

        return utilSchema.StatusOk(status="Korisnik uspjesno dodijeljen na predmet")
    except HAAMGenericError as e:
        return ErrorBase(errorCode=400, msg=e.msg)
    except Exception as e:
        print(e)
        return ErrorBase(
            errorCode=500, msg="Greska prilikom dodavanja korisnika na predmet"
        )


def delete_predmet(predmet_id: str, db: Session = Depends(get_db)):
    try:
        db.query(Predmet).filter(Predmet.id == predmet_id).delete()
        db.commit()
        return {"msg": "Predmet obrisan!"}
    except Exception as e:
        print(e)
        return ErrorBase(errorCode=500, msg="Error deleting predmet")


def get_predmeti_by_user_id(userId: str, db: Session = Depends(get_db)):
    try:
        predmeti = (
            db.query(PredmetKorisnik)
            .filter(PredmetKorisnik.korisnik_id == userId)
            .all()
        )
        if predmeti is None:
            return []
        predmetList = []
        for predmet in predmeti:
            predmetList.append(
                PredmetInDB(
                    id=predmet.predmet_id,
                    naziv=predmet.naziv_predmeta,
                    godinaStudija=0,
                )
            )
        return predmetList
    except Exception as e:
        print(e)
        return ErrorBase(errorCode=500, msg="Error fetching predmeti by user id")
