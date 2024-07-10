
from typing import Any
from pydantic import BaseModel, Field
from enum import Enum
from decouple import config
from langchain.agents import Tool
from langchain.utilities import BingSearchAPIWrapper
from langchain.utilities.wolfram_alpha import WolframAlphaAPIWrapper
from langchain.llms.replicate import Replicate



class ToolDescription(Enum):
    SEARCH = "useful for when you need to search for answers on the internet. You should ask targeted questions."
    WOLFRAM_ALPHA = "useful for when you need to do computation or calculation."


def get_search_tool() -> Any:
    search = BingSearchAPIWrapper(
        bing_search_url=config("BING_SEARCH_URL"),
        bing_subscription_key=config("BING_SUBSCRIPTION_KEY"),
    )

    return search


def get_wolfram_alpha_tool() -> Any:
    wolfram = WolframAlphaAPIWrapper()

    return wolfram

def get_replicate_tool(metadata: dict) -> Any:
    model = metadata["model"]
    api_token = metadata["api_key"]
    input = metadata["arguments"]
    model = Replicate(
        model=model,
        replicate_api_token=api_token if api_token else config("REPLICATE_API_TOKEN"),
        input=input,
    )
    
    return model