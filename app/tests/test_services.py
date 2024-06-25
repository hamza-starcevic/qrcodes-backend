import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.db.db_config import Base
from app.db.models.predavanje_model import Predavanje
from app.db.models.predavanjeKorisnik_model import PredavanjeKorisnik
from app.db.models.predmet_model import Predmet
from app.db.models.predmetKorisnik_model import PredmetKorisnik
from app.db.models.user_model import User
import uuid
import datetime

# Create a new engine instance for testing
DATABASE_URL = "postgresql://ajdin:ajdin@localhost:5432/qrcodes"
engine = create_engine(DATABASE_URL)

# Create a new session factory
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def setup_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    return db


def teardown_db(db: Session):
    db.close()
    Base.metadata.drop_all(bind=engine)


def create_sample_data(db: Session):
    user = User(
        id=uuid.uuid4(),
        email="testuser@example.com",
        first_name="Test",
        last_name="User",
        date_of_birth=datetime.date(1990, 1, 1),
        password="hashedpassword",
        role="student",
    )
    db.add(user)
    predmet = Predmet(id=uuid.uuid4(), naziv="Test Predmet", godina_studija=1)
    db.add(predmet)
    db.commit()
    db.refresh(user)
    db.refresh(predmet)
    return {"user": user, "predmet": predmet}


def test_create_predavanje():
    db = setup_db()
    sample_data = create_sample_data(db)

    try:
        from app.services.predavanjeService import create_predavanje
        from app.schemas.predavanjeSchema import PredavanjeBase

        predavanje_data = PredavanjeBase(
            predmet_id=sample_data["predmet"].id,
            broj_predavanja=1,
            datumPredavanja=datetime.date(1991, 1, 1),
            status="Nije odrzano",
        )
        predavanje = create_predavanje(predavanje_data, db)
        assert predavanje.id is not None
        assert predavanje.predmet_id == sample_data["predmet"].id
        assert predavanje.broj_predavanja == 1
        assert predavanje.status == "Nije odrzano"
    finally:
        teardown_db(db)


def test_generate_qrcode():
    db = setup_db()
    sample_data = create_sample_data(db)

    try:
        from app.services.predavanjeService import (
            create_predavanje,
            generate_qrcode,
        )
        from app.schemas.predavanjeSchema import PredavanjeBase

        predavanje_data = PredavanjeBase(
            predmet_id=sample_data["predmet"].id,
            broj_predavanja=1,
            status="Nije odrzano",
            datumPredavanja=datetime.date(1991, 1, 1),
        )
        predavanje = create_predavanje(predavanje_data, db)
        predavanje_with_qrcode = generate_qrcode(predavanje.id, db)
        assert predavanje_with_qrcode.qrcode is not None
    finally:
        teardown_db(db)


# Repeat similar modifications for other test functions...
