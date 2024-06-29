from fastapi import APIRouter, Depends, HTTPException, status

from app.lib.auth.prisma import JWTBearer, decodeJWT
from app.lib.documents import upsert_document
from app.lib.models.documents import Document
from app.lib.prisma import prisma

router = APIRouter()

@router.post("/documents", name="Create Doc", description="Create new doc")
async def create_document(body: Document, token=Depends(JWTBearer())):
    try:
        decoded = decodeJWT(token)
        document_type = body.type
        document_url = body.url
        document_name = body.name
        document = prisma.document.create(
            {
                "type": document_type,
                "url": document_url,
                "userId": decoded["userID"],
                "name": document_name
            }
        )

        upsert_document(
            url=document_url,
            type=document_type,
            document_id=document.id
        )

        return {"success": True, "data": document}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e
        )
    
@router.get("/documents", name="List documents", description="List all documents")
async def read_documents(token=Depends(JWTBearer())):
    """List documents endpoint"""
    decoded = decodeJWT(token)
    documents = prisma.document.find_many(
        where={"userId": decoded["userId"]}, include={"user": True}
    )

    if documents:
        return {"success": True, "data": documents}

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="No agents found",
    )


    
@router.get("/documents/{documentId}", name="Get Document", description="Get a doc")
async def read_document(documentId: str, token=Depends(JWTBearer())):
    """Get a single document"""
    document = prisma.document.find_unique(
        where={"id": documentId}, include={"user": True}
    )

    if document:
        return {"success": True, "data": document}

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Agent with id: {documentId} not found",
    )

@router.delete("/documents/{documentId}",name="Delete document",description="Delete a specific document",)
async def delete_document(documentId: str, token=Depends(JWTBearer())):
    """Delete a document"""
    try:
        prisma.document.delete(where={"id": documentId})

        return {"success": True, "data": None}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e,
        )