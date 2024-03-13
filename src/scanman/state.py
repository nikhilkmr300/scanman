from dataclasses import dataclass

from langchain.memory.chat_memory import BaseChatMemory

from .manpage import Manpage


@dataclass
class State:
    manpage: Manpage
    memory: BaseChatMemory
