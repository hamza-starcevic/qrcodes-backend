import uuid
from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.dialects.postgresql import UUID
from app.db.db_config import Base

class Predavanje(Base):
    __tablename__ = "predavanja"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, unique=True, default=uuid.uuid4)
    predmet_id = Column(UUID, ForeignKey('predmeti.id'), nullable=False)
    broj_predavanja = Column(Integer, nullable=False)
    qrcode = Column(String, nullable=True)
    status= Column(String, nullable=False, default="Nije odrzano")
    
    