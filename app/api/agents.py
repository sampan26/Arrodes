import json
import threading
from queue import Queue

from fastapi import APIRouter, Depends, HTTPException, status
from starlette.responses import StreamingResponse

from app.lib.agents import Agent as AgentDefinition
from app.lib.auth.prisma import JWTBearer, decodeJWT
from app.lib.models.agents import Agent, PredictAgent
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

@router.get("/agents/{agentId}", name="List all agents", description="List all agents")
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
    
@router.post("/agents/{agentId}/predict", name="Prompt agent", description="Invoke specific agent")
async def run_agent(agentId: str, body: PredictAgent):
    input = body.input
    has_streaming = body.has_streaming
    agent = await prisma.agent.find_unique(
        where={"id": agentId}, include={"user": True}
    )

    if agent:
        if has_streaming:

            def on_llm_new_token(token):
                data_queue.put(token)
            
            def on_llm_end():
                data_queue.put("[END]")

            def event_stream(data_queue: Queue) -> str:
                while True:
                    data = data_queue.get()
                    if data == "[END]":
                        yield f"data:{data} \n\n"
                        break 
                    yield f"data:{data} \n\n"
            
            def conversation_run_thread(input: dict) -> None:
                agent_definition = AgentDefinition(
                    agent=agent,
                    has_streaming=has_streaming,
                    on_llm_new_token=on_llm_new_token,
                    on_llm_end=on_llm_end,
                )
                agent_executor = agent_definition.get_agent()
                agent_executor.run(input)

            data_queue = Queue()
            t = threading.Thread(target=conversation_run_thread, args=(input,))
            t.start()
            response = StreamingResponse(event_stream(data_queue), media_type="text/event-stream")
            return response
        
        agent_definition = AgentDefinition(
            agent=agent,
            has_streaming=has_streaming,
        )
        agent_executor = agent_definition.get_agent()
        output = await agent_executor.arun(input)

        return {"success": True, "data": output}

    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Agent with id: {agentId} not found",
    )