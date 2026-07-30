from fastapi import FastAPI

from app.api.repository import router as repository_router
from app.core.config import settings
from app.db.base import Base
from app.db.database import engine

# Import models so SQLAlchemy knows about them
from app.models.repository import Repository

app = FastAPI(
    title=settings.APP_NAME,
)
app.include_router(repository_router)

# Create all tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {
        "message": f"Welcome to {settings.APP_NAME} 🚀",
        "environment": settings.ENVIRONMENT,
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }