from typing import Any

from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI

from app.lib.callbacks import StreamingCallbackHandler
from app.lib.prompts import default_chat_prompt

class Agent:
    def __init__(
            self,
            agent: dict,
            has_streaming: bool = False,
            on_llm_new_token=None,
            on_llm_end=None,
    ):
        self.id = agent.id
        self.has_memory = agent.hasMemory
        self.type = agent.type
        self.llm = agent.llm
        self.prompt = default_chat_prompt
        self.has_streaming = has_streaming
        self.on_llm_new_token = on_llm_new_token
        self.on_llm_end = on_llm_end

    def _get_llm(self) -> Any:
        if self.llm["provider"] == "openai-chat":
            return (
                ChatOpenAI(
                    model_name=self.llm["model"],
                    streaming=self.has_streaming,
                    callbacks=[
                        StreamingCallbackHandler(
                            on_new_token=self.on_llm_new_token, on_end = self.on_llm_end
                        )
                    ],
                )
                if self.has_streaming
                else ChatOpenAI(model_name=self.llm["model"])
            )
        
        if self.llm["provider"] == "openai":
            return OpenAI(model_name=self.llm["model"])
        
        return ChatOpenAI(temperature=0)

    def _get_memory(self) -> None:
        if self.has_memory:
            print("Agent has memory")

        return None
    
    def get_agent(self) -> Any:
        llm = self._get_llm()
        agent = LLMChain(llm=llm, verbose=True, prompt=self.prompt)

        return agent