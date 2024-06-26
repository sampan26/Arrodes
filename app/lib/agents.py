from typing import Any

from langchain.chains import ConversationalRetrievalChain, LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.memory import ChatMessageHistory, ConversationBufferMemory
from langchain.vectorstores.pinecone import Pinecone

from app.lib.callbacks import StreamingCallbackHandler
from app.lib.prisma import prisma
from app.lib.prompts import default_chat_prompt

class Agent:
    def __init__(
            self,
            agent: dict,
            has_streaming: bool = False,
            on_llm_new_token=None,
            on_llm_end=None,
            on_chain_end=None,
    ):
        self.id = agent.id
        self.document = agent.document
        self.has_memory = agent.hasMemory
        self.type = agent.type
        self.llm = agent.llm
        self.prompt = default_chat_prompt
        self.has_streaming = has_streaming
        self.on_llm_new_token = on_llm_new_token
        self.on_llm_end = on_llm_end
        self.on_chain_end= on_chain_end

    async def _get_llm(self) -> Any:
        if self.llm["provider"] == "openai-chat":
            return (
                ChatOpenAI(
                    model_name=self.llm["model"],
                    streaming=self.has_streaming,
                    callbacks=[
                        StreamingCallbackHandler(
                            on_new_token=self.on_llm_new_token, 
                            on_end = self.on_llm_end,
                            on_chain_end = self.on_chain_end,
                        )
                    ],
                )
                if self.has_streaming
                else ChatOpenAI(model_name=self.llm["model"])
            )
        
        if self.llm["provider"] == "openai":
            return OpenAI(model_name=self.llm["model"])
        
        return ChatOpenAI(temperature=0)

    async def _get_memory(self) -> Any:
        if self.has_memory:
            memories = await prisma.agentmemory.find_many(
                where={"agentId": self.id},
                order={"createdAt": "desc"},
                take=5,
            )
            history = ChatMessageHistory()
            [
                history.add_ai_message(memory.message)
                if memory.agent == "AI"
                else history.add_user_message(memory.message)
                for memory in memories
            ]
            memory = ConversationBufferMemory(chat_memory=history, memory_key="chat_history")

            return memory

        return None
    
    async def _get_document(self) -> Any:
        if self.document:
            embeddings = OpenAIEmbeddings()
            docsearch = Pinecone.from_existing_index(
                "arrodes", embeddings=embeddings, namespace=self.document.id
            )

            return docsearch
        
        return None

    async def get_agent(self) -> Any:
        llm = await self._get_llm()
        memory = await self._get_memory()
        document = await self._get_document()
        if document:
            agent = ConversationalRetrievalChain.from_llm(
                llm=llm,
                retriever=document.as_retriever(),
                memory=memory,
                verbose=True,
                get_chat_history=lambda h: h,
            )
        else:
            agent = LLMChain(llm=llm, memory=memory, verbose=True, prompt=self.prompt)

        return agent