from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"Starting {settings.APP_NAME}...")
    yield
    print(f"Shutting down {settings.APP_NAME}...")


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        lifespan=lifespan
    )
    
    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "service": settings.APP_NAME}
    
    return app



app = create_app()