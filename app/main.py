from fastapi import FastAPI
from app.api.routes import router

from contextlib import asynccontextmanager
from app.services.vector_service import create_collection


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_collection()

    yield

    print("Application shutting down...")

app = FastAPI(lifespan=lifespan)

app.include_router(router)