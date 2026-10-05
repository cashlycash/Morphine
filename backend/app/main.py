import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from app.api.v1.routes import router as v1_router
from app.core.config import get_settings
from app.db.base import Base
from app.db.session import engine

settings = get_settings()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.app_name, version=settings.app_version)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(v1_router)
Instrumentator().instrument(app).expose(app)


@app.on_event("startup")
def startup() -> None:
    logger.info("Starting Morphine API")
    Base.metadata.create_all(bind=engine)


@app.get("/healthz")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
