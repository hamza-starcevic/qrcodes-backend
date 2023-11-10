# db_init.py
import logging
from app.db.models.user import User
from app.db.db_config import engine, Base


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('sqlalchemy.engine')
def init_db():
    Base.metadata.create_all(bind=engine)

init_db()