from fastapi import HTTPException
from ..core.rag_engine import StudyBuddyRAG

# Global RAG instance
_rag_engine: StudyBuddyRAG


def set_rag_engine(engine: StudyBuddyRAG):
    """Set the global RAG engine instance"""
    global _rag_engine
    _rag_engine = engine


def get_rag_engine() -> StudyBuddyRAG:
    """Get the global RAG engine instance"""
    if _rag_engine is None:
        raise HTTPException(status_code=503, detail="RAG engine not initialized")
    return _rag_engine
