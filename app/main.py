from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logger import log
from app.api import router


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="ASR (Automatic Speech Recognition) Service API",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router, prefix="/api")

    @app.on_event("startup")
    async def startup_event():
        log.info(f"{settings.APP_NAME} v{settings.APP_VERSION} starting up...")
        log.info(f"Debug mode: {settings.DEBUG}")

    @app.on_event("shutdown")
    async def shutdown_event():
        log.info(f"{settings.APP_NAME} shutting down...")

    @app.get("/")
    async def root():
        res = {
            "name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "status": "running",
            "docs": "/docs"
        }
        log.info(f"Root endpoint accessed: {res}")
        return res

    @app.get("/health")
    async def health():
        res = {
            "status": "healthy",
            "version": settings.APP_VERSION
        }
        log.info(f"Health endpoint accessed: {res}")
        return res

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )