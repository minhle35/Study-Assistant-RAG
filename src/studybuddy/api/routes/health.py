from fastapi import APIRouter, Depends
from ...models.responses import HealthResponse
from ...config import settings
from ..dependencies import get_rag_engine
from ...core.rag_engine import StudyBuddyRAG

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check(rag_engine: StudyBuddyRAG = Depends(get_rag_engine)):
    """Health check endpoint"""
    docs = rag_engine.get_documents_info()
    return HealthResponse(
        status="healthy",
        documents_count=len(docs),
        documents=docs,
        version=settings.version,
    )
