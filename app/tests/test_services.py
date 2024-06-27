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
import bcrypt
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


def create_sample_data(db: Session):
    user = User(
        id=uuid.uuid4(),
        email="testuser@example.com" + str(uuid.uuid4()),
        first_name="Test",
        last_name="User",
        date_of_birth=datetime.date(1990, 1, 1),
        password="hashedpassword",
        role="student",
    )
    db.add(user)
    predmet = Predmet(
        id=uuid.uuid4(), naziv="Test Predmet" + str(uuid.uuid4()), godina_studija=1
    )
    db.add(predmet)
    db.commit()
    db.refresh(user)
    db.refresh(predmet)
    return {"user": user, "predmet": predmet}


# Predmet Service Tests


def test_create_predmet():
    db = setup_db()

    try:
        from app.services.predmetService import create_predmet
        from app.schemas.predmetSchema import PredmetBase

        predmet_data = PredmetBase(naziv="Test Predmet", godinaStudija=1)
        predmet = create_predmet(predmet_data, db)
        assert predmet.id is not None
        assert predmet.naziv == "Test Predmet"
        assert predmet.godinaStudija == 1
    finally:
        teardown_db(db)


def test_get_predmeti():
    db = setup_db()
    create_sample_data(db)

    try:
        from app.services.predmetService import get_predmeti

        predmeti = get_predmeti(db)
        assert len(predmeti) > 0
    finally:
        teardown_db(db)


def test_add_korisnik_to_predmet():
    db = setup_db()
    sample_data = create_sample_data(db)

    try:
        from app.services.predmetService import add_korisnik
        from app.schemas.predmetKorisniciSchema import PredmetKorisnikCreateDTO

        add_korisnik_data = PredmetKorisnikCreateDTO(
            predmetId=sample_data["predmet"].id, korisnikId=sample_data["user"].id
        )
        result = add_korisnik(add_korisnik_data, db)
        assert result.status == "Korisnik uspjesno dodijeljen na predmet"
    finally:
        teardown_db(db)


def test_delete_predmet():
    db = setup_db()
    sample_data = create_sample_data(db)

    try:
        from app.services.predmetService import delete_predmet

        delete_result = delete_predmet(sample_data["predmet"].id, db)
        assert delete_result["msg"] == "Predmet obrisan!"
    finally:
        teardown_db(db)


# User Service Tests


def test_create_user():
    db = setup_db()

    try:
        from app.services.userServices import create_user
        from app.schemas.userSchema import UserCreate

        rand_attachment = str(uuid.uuid4)
        user_data = UserCreate(
            email="newuser@example.com" + rand_attachment,
            firstName="New",
            lastName="User",
            dateOfBirth=datetime.date(1995, 1, 1),
            password="newpassword",
            role="student",
        )
        user = create_user(user_data, db)
        print(user)
        assert user.id is not None
        assert user.email == "newuser@example.com" + rand_attachment
    finally:
        teardown_db(db)


def test_login_user():
    db = setup_db()
    sample_data = create_sample_data(db)

    try:
        from app.services.userServices import login_user
        from app.schemas.userSchema import UserLogin

        login_data = UserLogin(
            email=sample_data["user"].email, password="hashedpassword"
        )
        login_result = login_user(login_data, db)
        print(login_result)
        assert login_result.token is not None
    finally:
        teardown_db(db)


def test_get_users():
    db = setup_db()
    create_sample_data(db)

    try:
        from app.services.userServices import get_users

        users = get_users(db)
        assert len(users) > 0
    finally:
        teardown_db(db)


def test_delete_user():
    db = setup_db()
    sample_data = create_sample_data(db)

    try:
        from app.services.userServices import delete_user

        delete_result = delete_user(sample_data["user"].id, db)
        assert delete_result.status == "User deleted"
    finally:
        teardown_db(db)


def test_get_users_by_role():
    db = setup_db()
    create_sample_data(db)

    try:
        from app.services.userServices import get_users_by_role

        users = get_users_by_role("student", db)
        assert len(users) > 0
    finally:
        teardown_db(db)
