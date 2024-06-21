from typing import Any, Dict, List, Optional, Union

from langchain.callbacks.base import AsyncCallbackHandler
from langchain.schema import AgentAction, AgentFinish, LLMResult

class StreamingCallbackHandler(AsyncCallbackHandler):

    def __init__(self, on_llm_new_token_, on_llm_end_, on_chain_end_) -> None:
        self.on_llm_new_token_ = on_llm_new_token_
        self.on_llm_end_ = on_llm_end_
        self.on_chain_end_ = on_chain_end_

    def on_llm_start(
            self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        pass

    async def on_llm_new_token(self, token: str, *args, **kwargs: Any) -> None:
        await self.on_llm_new_token_(token)

    async def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        await self.on_llm_end_()

    def on_llm_error(
        self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> None:
        pass

    def on_chain_start(
        self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
    ) -> None:
        pass

    async def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        print(outputs, kwargs)
        await self.on_chain_end_(outputs)

    def on_tool_start(
        self,
        serialized: Dict[str, Any],
        input_str: str,
        **kwargs: Any,
    ) -> None:
        pass

    def on_agent_action(self, action: AgentAction, **kwargs: Any) -> Any:
        # st.write requires two spaces before a newline to render it
        pass

    def on_tool_end(
        self,
        output: str,
        observation_prefix: Optional[str] = None,
        llm_prefix: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        pass

    def on_tool_error(
        self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> None:
        pass

    def on_text(self, text: str, **kwargs: Any) -> None:
        # st.write requires two spaces before a newline to render it
        pass

    def on_agent_finish(self, finish: AgentFinish, **kwargs: Any) -> None:
        # st.write requires two spaces before a newline to render it
        pass