import uuid
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.dialects.postgresql import UUID
from app.db.db_config import Base

class Predmet(Base):
    __tablename__ = "predmeti"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, unique=True, default=uuid.uuid4)
    naziv = Column(String(), nullable=False)
    godina_studija = Column(Integer(), nullable=True)
    