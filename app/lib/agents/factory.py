from app.lib.agents.agent import (
    DefaultAgent,
    DocumentAgent,
    OpenApiDocumentAgent,
    OpenAIAgent,
    ToolAgent,
)


class AgentFactory:
    @staticmethod
    def create_agent(agent_base):
        if agent_base.document:
            if agent_base.document.type == "OPENAPI":
                return OpenApiDocumentAgent(agent_base)

            return DocumentAgent(agent_base)

        elif agent_base.tool:
            if agent_base.type == "OPENAI":
                return OpenAIAgent(agent_base)
            
            return ToolAgent(agent_base)

        else:
            return DefaultAgent(agent_base)