import argparse
import logging
import sys

from langchain.memory import ConversationBufferWindowMemory
from termcolor import colored

from .commands import Command
from .manpage import Manpage
from .rag import ERROR_MSG, ask, load_retriever
from .state import State

PROMPT_BASE = "scanman"
PROMPT_COLOR = "blue"


def prompt(manpage=None):
    content = ""
    if not manpage:
        content = colored(f"{PROMPT_BASE}> ", PROMPT_COLOR, attrs=["bold"])
    else:
        content = colored(
            f"{PROMPT_BASE}/{manpage.name}> ", PROMPT_COLOR, attrs=["bold"]
        )
    return str(input(content))


def cli():
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.ERROR)
    logger.setLevel(logging.ERROR)

    argparser = argparse.ArgumentParser(prog="scanman")
    argparser.add_argument("manpage")
    args = argparser.parse_args()

    state = State(
        Manpage(args.manpage),
        ConversationBufferWindowMemory(k=50, return_messages=True),
    )

    while True:
        input_ = prompt(manpage=state.manpage).split(" ")

        if Command.is_command(input_[0]):
            cmd_name, cmd_args = input_[0], input_[1:]

            try:
                cmd = Command.parse(cmd_name)
                cmd.execute(cmd_args, state)  # This command may change state.

            except ValueError:
                sys.stderr.write(
                    colored(f"{cmd_name} is not a valid command.\n", "red")
                )

        else:
            query = " ".join(input_).strip()

            logger.debug(
                f"manpage={state.manpage.name}, memory={state.memory.chat_memory}"
            )

            retriever = load_retriever(state.manpage)
            response = ask(query, retriever, state.memory)["answer"]

            state.memory.chat_memory.add_user_message(query)
            state.memory.chat_memory.add_ai_message(response)

            if ERROR_MSG in response:
                print(colored(response, "red"))
            else:
                print(colored(response, "green"))
