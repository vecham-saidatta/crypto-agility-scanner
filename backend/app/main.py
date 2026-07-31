from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.repository import router as repository_router
from app.core.config import settings
from app.db.base import Base
from app.db.database import engine
from app.api import scan
# Import models so SQLAlchemy knows about them
from app.models.repository import Repository

app = FastAPI(
    title=settings.APP_NAME,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(repository_router)
app.include_router(scan.router)

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