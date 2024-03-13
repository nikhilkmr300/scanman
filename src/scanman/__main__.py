import argparse
import logging
import os
import readline
import sys

from langchain.memory import ConversationBufferWindowMemory
from termcolor import colored

from .cli import prompt
from .commands import Command
from .manpage import Manpage
from .rag import ERROR_MSG, ask, load_retriever
from .state import State

def main():
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.ERROR)
    logger.setLevel(logging.ERROR)

    argparser = argparse.ArgumentParser(prog=os.path.basename(__file__))
    argparser.add_argument("manpage")
    args = argparser.parse_args()

    state = State(
        Manpage(args.manpage),
        ConversationBufferWindowMemory(k=50, return_messages=True)
    )

    while True:
        input_ = prompt(manpage=state.manpage).split(" ")

        if Command.is_command(input_[0]):
            cmd_name, cmd_args = input_[0], input_[1:]

            try:
                cmd = Command.parse(cmd_name)
                cmd.execute(cmd_args, state)   # This command may change state.

            except ValueError:
                sys.stderr.write(colored(f"{cmd_name} is not a valid command.\n", "red"))

        else:
            query = " ".join(input_).strip()

            logger.debug(f"manpage={state.manpage.name}, memory={state.memory.chat_memory}")

            retriever = load_retriever(state.manpage)
            response = ask(query, retriever, state.memory)["answer"]

            state.memory.chat_memory.add_user_message(query)
            state.memory.chat_memory.add_ai_message(response)

            if ERROR_MSG in response:
                print(colored(response, "red"))
            else:
                print(colored(response, "green"))


if __name__ == "__main__":
    main()