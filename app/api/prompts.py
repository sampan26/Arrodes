import json

from fastapi import APIRouter, Depends

from app.lib.auth.prisma import JWTBearer, decodeJWT
from app.lib.models.prompt import Prompt
from app.lib.prisma import prisma

router = APIRouter()

@router.post("/prompts", name="Create a prompt", description="Create a new prompt")
async def create_prompt(body: Prompt, token=Depends(JWTBearer())):
    decoded = decodeJWT(token)

    prompt = prisma.prompt.create(
        {
            "name": body.name,
            "input_variables": json.dump(body.input_variables),
            "template": body.template,
            "userId": decoded["userId"],
        },
        include={"user": True}
    )

    return {"success": True, "data": prompt}

@router.get("/prompts", name="List prompts", description="List all prompts")
async def read_prompts(token=Depends(JWTBearer())):
    decoded = decodeJWT(token)
    prompt = prisma.prompt.find_many(
        where={"userId": decoded["userId"]}, include={"user": True}
    )

    return {"success": True, "data": prompt}

@router.get("/prompts/{promptId}", name="Get prompt", description="Get a specific prompt")
async def read_prompt(promptId: str, token=Depends(JWTBearer())):
    prompt = prisma.prompt.find_unique(where={"id": promptId}, include={"user": True})
    return {"success": True, "data": prompt}

@router.delete("/prompt/{promptId}", name="Delete prompt", description="Delete a specifi prompt")
async def delete_prompt(promptId: str, token=Depends(JWTBearer())):
    prisma.prompt.delete(where={"id": promptId})
    return {"success": True, "data": None}

 