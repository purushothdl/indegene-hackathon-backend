from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database.mongodb import mongodb
from app.core.error_handler import global_exception_handler
from app.routes.files import file_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await mongodb.connect()
    yield
    await mongodb.close()

app = FastAPI(lifespan=lifespan)
app.add_exception_handler(Exception, global_exception_handler)

app.include_router(file_router)