from fastapi import APIRouter, Depends, HTTPException
from ...models.requests import ChatRequest
from ...models.responses import ChatResponse
from ..dependencies import get_rag_engine
from ...core.rag_engine import StudyBuddyRAG

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest, rag_engine: StudyBuddyRAG = Depends(get_rag_engine)
):
    """Chat with StudyBuddy"""
    try:
        result = await rag_engine.answer_question(
            question=request.question, max_sources=request.max_sources
        )

        return ChatResponse(
            answer=result["answer"],
            sources=result["sources"] if request.include_sources else [],
            study_tips=result["study_tips"],
            response_time=result["response_time"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
