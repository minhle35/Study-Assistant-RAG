from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .core.rag_engine import StudyBuddyRAG
from .api.dependencies import set_rag_engine
from .api.routes import health, chat, documents


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    print(f"🚀 Starting {settings.app_name}...")
    rag_engine = StudyBuddyRAG()
    await rag_engine.initialize()
    set_rag_engine(rag_engine)
    print("✅ StudyBuddy ready!")

    yield

    # Shutdown
    print("🛑 Shutting down StudyBuddy...")
    await rag_engine.cleanup()


def create_app() -> FastAPI:
    """Create FastAPI application"""
    app = FastAPI(
        title=settings.app_name,
        version=settings.version,
        description="AI-powered study assistant with RAG capabilities",
        lifespan=lifespan,
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(health.router, prefix="/api/v1", tags=["Health"])
    app.include_router(chat.router, prefix="/api/v1", tags=["Chat"])
    app.include_router(documents.router, prefix="/api/v1", tags=["Documents"])

    @app.get("/")
    async def root():
        return {
            "message": f"{settings.app_name} is running! 📚🤖",
            "version": settings.version,
            "docs": "/docs",
        }

    return app


# Create app instance
app = create_app()
