import uuid
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.db.db_config import Base

class PredmetKorisnik(Base):
    __tablename__ = "predmeti_korisnici"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, unique=True, default=uuid.uuid4)
    predmet_id = Column(UUID, ForeignKey('predmeti.id'), nullable=False)
    korisnik_id = Column(UUID, ForeignKey('users.id'), nullable=False)
    role = Column(String, nullable=False)