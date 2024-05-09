from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import root_router
from src.core import settings
from src.dependencies import init_dependencies


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # you can do some initialization here
    yield


def init_routers(_app: FastAPI):
    app.include_router(root_router)


app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
    version=settings.app_version,
    lifespan=lifespan,
)
app.include_router(root_router)
init_dependencies(app)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
