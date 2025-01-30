from pydantic import BaseModel, EmailStr


class SUser(BaseModel):
    username: str
    name: str | None = None
    email: EmailStr | None = None
    hash_password: str
