import logging
import sys

from langchain.memory import ConversationBufferWindowMemory

from .manpage import Manpage, ManpageNotFoundException

SIGIL = ":"

logger = logging.getLogger("scanman")


class Command:
    def execute(self, args, state):
        pass

    @staticmethod
    def is_command(cmd_name):
        return cmd_name.startswith(SIGIL)

    @staticmethod
    def parse(cmd_name):
        if cmd_name == Change.name:
            return Change()
        elif cmd_name == Exit.name:
            return Exit()
        else:
            raise ValueError(f"`{cmd_name}` is not a valid command.")


class Change(Command):
    name = f"{SIGIL}change"

    def execute(self, args, state):
        try:
            manpage = Manpage(args[0])

            # Refreshing man page, memory and retriever
            state.manpage = manpage
            logger.info(f"Changed manpage to `{state.manpage.name}`.")
            state.memory = ConversationBufferWindowMemory(k=50)
            logger.info("Refreshed LLM memory.")
            state.retriever = None
            logger.info("Refreshed retriever.")

        except ManpageNotFoundException:
            sys.stderr.write(f"Could not find manpage `{args[0]}`.\n")


class Exit(Command):
    name = f"{SIGIL}exit"

    def execute(self, args, state):
        sys.exit(0)
