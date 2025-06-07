from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class SourceDocument(BaseModel):
    """Source document reference"""

    filename: str
    content_snippet: str
    relevance_score: float
    page_number: Optional[int] = None


class ChatResponse(BaseModel):
    """Chat response model"""

    answer: str
    sources: List[SourceDocument] = []
    study_tips: List[str] = []
    response_time: float


class DocumentInfo(BaseModel):
    """Document information"""

    filename: str
    chunk_count: int
    subject: str
    upload_date: Optional[datetime] = None
    size_bytes: Optional[int] = None


class HealthResponse(BaseModel):
    """Health check response"""

    status: str
    documents_count: int
    documents: List[DocumentInfo]
    version: str
    uptime: Optional[float] = None
