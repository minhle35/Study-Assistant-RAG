from fastapi import APIRouter, UploadFile, File, HTTPException, Depends

from ...config import settings
from ..dependencies import get_rag_engine
from ...core.rag_engine import StudyBuddyRAG

router = APIRouter()


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...), rag_engine: StudyBuddyRAG = Depends(get_rag_engine)
):
    """Upload a new document"""
    if not file.filename.endswith(tuple(settings.supported_extensions)):
        raise HTTPException(
            status_code=400,
            detail=f"Only {', '.join(settings.supported_extensions)} files are supported",
        )

    # Save file
    file_path = settings.documents_dir / file.filename
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # Process the document
    await rag_engine._process_single_document(file_path)

    return {"message": f"Document {file.filename} uploaded and processed successfully"}
