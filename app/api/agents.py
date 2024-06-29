import asyncio
import json
import threading
from queue import Queue
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.api_key import APIKey
from starlette.responses import StreamingResponse

from app.lib.agents import Agent as AgentDefinition
from app.lib.auth.api import get_api_key
from app.lib.auth.prisma import JWTBearer, decodeJWT
from app.lib.models.agent import Agent, PredictAgent
from app.lib.prisma import prisma

router = APIRouter()


@router.post("/agents", name="Create agent", description="Create a new agent")
async def create_agent(body: Agent, token=Depends(JWTBearer())):
    """Agents endpoint"""
    decoded = decodeJWT(token)

    try:
        agent = prisma.agent.create(
            {
                "name": body.name,
                "type": body.type,
                "llm": json.dumps(body.llm),
                "hasMemory": body.has_memory,
                "userId": decoded["userId"],
                "documentId": body.documentId,
                "promptId": body.promptId,
            },
            include={"user": True},
        )

        return {"success": True, "data": agent}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e,
        )


@router.get("/agents", name="List all agents", description="List all agents")
async def read_agents(token=Depends(JWTBearer())):
    """Agents endpoint"""
    decoded = decodeJWT(token)
    agents = prisma.agent.find_many(
        where={"userId": decoded["userId"]},
        include={
            "user": True,
            "document": True,
            "prompt": True,
        },
        order={"createdAt": "desc"},
    )

    if agents:
        return {"success": True, "data": agents}

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="No agents found",
    )


@router.get("/agents/{agentId}", name="Get agent", description="Get a specific agent")
async def read_agent(agentId: str, token=Depends(JWTBearer())):
    """Agent detail endpoint"""
    agent = prisma.agent.find_unique(where={"id": agentId}, include={"user": True})

    if agent:
        return {"success": True, "data": agent}

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Agent with id: {agentId} not found",
    )


@router.delete("/agents/{agentId}", name="Delete agent", description="Delete a specific agent")
async def delete_agent(agentId: str, token=Depends(JWTBearer())):
    """Delete agent endpoint"""
    try:
        prisma.agentmemory.delete_many(where={"agentId": agentId})
        prisma.agent.delete(where={"id": agentId})

        return {"success": True, "data": None}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e,
        )


@router.patch("/agents/{agentId}", name="Delete agent", description="Delete a specific agent")
async def patch_agent(agentId: str, body: dict, token=Depends(JWTBearer())):
    """Patch agent endpoint"""
    try:
        prisma.agent.update(data=body, where={"id": agentId})

        return {"success": True, "data": None}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e,
        )


@router.post("/agents/{agentId}/predict", name="Prompt agent", description="Invoke a specific agent",)
async def run_agent(
    agentId: str, body: PredictAgent, api_key: APIKey = Depends(get_api_key)
):
    """Agent detail endpoint"""
    input = body.input
    input["chat_history"] = []
    has_streaming = body.has_streaming
    agent = prisma.agent.find_unique(
        where={"id": agentId}, include={"user": True, "document": True, "prompt": True}
    )

    prisma.agentmemory.create(
        {
            "author": "HUMAN",
            "message": input.get("human_input", input.get("question", "")),
            "agentId": agentId,
        }
    )

    if agent:
        if has_streaming:

            def on_llm_new_token(token) -> None:
                data_queue.put(token)

            def on_llm_end() -> None:
                data_queue.put("[END]")

            def on_chain_end(outputs: Dict[str, Any]) -> None:
                pass

            def event_stream(data_queue: Queue) -> str:
                ai_message = ""
                while True:
                    data = data_queue.get()
                    ai_message += data
                    if data == "[END]":
                        prisma.agentmemory.create(
                            {"author": "AI", "message": ai_message, "agentId": agentId}
                        )
                        yield f"data: {data}\n\n"
                        break
                    yield f"data: {data}\n\n"

            def conversation_run_thread(input: dict) -> None:
                agent_definition = AgentDefinition(
                    agent=agent,
                    has_streaming=has_streaming,
                    on_llm_new_token=on_llm_new_token,
                    on_llm_end=on_llm_end,
                    on_chain_end=on_chain_end,
                )
                agent_executor = agent_definition.get_agent()
                agent_executor.run(input)

            data_queue = Queue()
            threading.Thread(target=conversation_run_thread,args=(input,)).start()
            response = StreamingResponse(
                event_stream(data_queue), media_type="text/event-stream"
            )

            return response

        else:
            agent_definition = AgentDefinition(agent=agent, has_streaming=has_streaming)
            agent_executor = agent_definition.get_agent()
            output = agent_executor.run(input)
            prisma.agentmemory.create(
                {"author": "AI", "message": output, "agentId": agentId}
            )

            return {"success": True, "data": output}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Agent with id: {agentId} not found",
    )