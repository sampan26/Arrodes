import json

from fastapi import APIRouter, Depends, HTTPException, status

from app.lib.auth.prisma import JWTBearer, decodeJWT
from app.lib.models.agents import Agent
from app.lib.prisma import prisma

router = APIRouter()


@router.post("/agents/", name="Create agent", description="Create a new agent")
async def create_agents(body: Agent, token = Depends(JWTBearer())):
    """Agents endpoint"""
    decoded = decodeJWT(token)

    try:
        agent = await prisma.agent.create(
            {
                "name": body.name,
                "type": body.type,
                'llm': json.dumps(body.llm),
                "userId": decoded["userId"]
            },
            include={"user": True},
        )
        return {"success": True, "data": agent}
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e
        )
    
@router.get("/agents", name="Create agent", description="Create a new agent")
async def read_agents(token=Depends(JWTBearer())):
    decoded = decodeJWT(token)
    agents = await prisma.agent.find_many(
        where={"userId": decoded["userId"]}, include={"user": True}
    )

    if agents:
        return {"success": True, "data": agents}
    
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="no agent found"
    )

@router.get("/agents/{agentId}", name="Get agent", description="Get a specific agent")
async def read_agent(agentId: str, token=Depends(JWTBearer())):
    agent = await prisma.agent.find_unique(
        where={"id": agentId}, include={"user": True}
    )

    if agent:
        return {"success": True, "data": agent}
    
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Agent with id {agentId} not found"
    )

@router.delete(
    "/agents/{agentId}", name="Delete agent", description="Delete a specific agent"
)
async def delete_agent(agentId: str, token=Depends(JWTBearer())):
    try:
        await prisma.agent.delete(where={"id": agentId})

        return {"success": True, "data": None}
    except Exception as e:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e
        )