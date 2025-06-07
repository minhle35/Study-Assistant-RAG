from pydantic import BaseModel, Field
from typing import Optional


class ChatRequest(BaseModel):
    """Chat request model"""

    question: str = Field(..., min_length=1, max_length=1000)
    include_sources: bool = True
    max_sources: int = Field(default=3, ge=1, le=10)


class DocumentUploadRequest(BaseModel):
    """Document upload metadata"""

    subject: Optional[str] = "general"
    description: Optional[str] = None
