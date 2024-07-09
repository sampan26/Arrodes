from pydantic import BaseModel

class AgentDocument(BaseModel):
    agentId: str
    document_id: str