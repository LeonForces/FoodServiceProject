from src.db.postgres import Base
from sqlalchemy import Column, UUID, String
from uuid import uuid4


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    login = Column(String(50), unique=True, nullable=False)
    name = Column(String(50))
    email = Column(String(50))
    password_hash = Column(String(50), nullable=False)
