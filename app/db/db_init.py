# db_init.py
import logging
from app.db.models.user_model import User
from app.db.models.predmet_model import Predmet
from app.db.models.predmetKorisnik_model import PredmetKorisnik
from app.db.models.predavanje_model import Predavanje
from app.db.models.predavanjeKorisnik_model import PredavanjeKorisnik
from app.db.db_config import engine, Base


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sqlalchemy.engine")


def init_db():
    Base.metadata.create_all(bind=engine)


init_db()
