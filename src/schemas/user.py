from pydantic import BaseModel, EmailStr
import uuid


class UserBase(BaseModel):
    id: uuid.UUID
    login: str
    name: str | None
    email: EmailStr | None
    password: str
