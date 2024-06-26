from fastapi import APIRouter, Depends, HTTPException, status

from app.lib.auth.prisma import JWTBearer, decodeJWT
from app.lib.documents import upsert_document
from app.lib.models.documents import Document
from app.lib.prisma import prisma

router = APIRouter()

@router.post("/documents/", name="Create Doc", description="Create new doc")
async def create_document(body: Document, token=Depends(JWTBearer())):
    try:
        decoded = decodeJWT(token)
        document_type = body.type
        document_url = body.url
        document = await prisma.document.create(
            {"type": document_type, "url": document_url, "userID": decoded["userID"]}
        )

        await upsert_document(url=document_url, type=document_type, document_id=document.id)

        return {"success": True, "data": document}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e
        )
    
@router.get("/documents/{documentId}", name="Get Document", description="Get a doc")
async def read_document(documentId: str, token=Depends(JWTBearer())):
    """Get a single document"""
    document = await prisma.document.find_unique(
        where={"id": documentId}, include={"user": True}
    )

    if document:
        return {"success": True, "data": document}

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Agent with id: {documentId} not found",
    )

@router.delete(
    "/agents/{documentId}",
    name="Delete document",
    description="Delete a specific document",
)
async def delete_document(documentId: str, token=Depends(JWTBearer())):
    """Delete a document"""
    try:
        await prisma.agent.delete(where={"id": documentId})

        return {"success": True, "data": None}
    except Exception as e:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e,
        )