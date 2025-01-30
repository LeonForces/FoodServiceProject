from sqlalchemy import Column, UUID, String
from uuid import uuid4

from src.db.postgres import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    username = Column(String(50), unique=True, nullable=False)
    name = Column(String(50), nullable=True)
    email = Column(String(50), nullable=True)
    hash_password = Column(String(255), nullable=False)
