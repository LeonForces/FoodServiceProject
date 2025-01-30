from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.db.postgres import create_tables, drop_tables
from src.api.v1.auth import router as auth
from src.api.v1.users import router as users


@asynccontextmanager
async def lifespan(_: FastAPI):
    await drop_tables()
    await create_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth)
app.include_router(users)
