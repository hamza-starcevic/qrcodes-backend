import uuid
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.dialects.postgresql import UUID
from app.db.db_config import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, unique=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    date_of_birth = Column(Date)
    password = Column(String)
    role = Column(String)