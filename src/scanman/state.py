from dataclasses import dataclass

from langchain.memory.chat_memory import BaseChatMemory
from langchain_core.retrievers import BaseRetriever

from .manpage import Manpage


@dataclass
class State:
    manpage: Manpage
    memory: BaseChatMemory
    retriever: BaseRetriever
