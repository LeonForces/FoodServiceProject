from fastapi import FastAPI
from typing import Union
from contextlib import asynccontextmanager
from src.db.postgres import create_tables, drop_tables


@asynccontextmanager
async def lifespan(_: FastAPI):
    await drop_tables()
    await create_tables()

    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
