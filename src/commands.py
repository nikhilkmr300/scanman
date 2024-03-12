import sys
from manpage import Manpage, ManpageNotFoundException

from state import load_state, save_state

SIGIL = ":"


class Command:
    def execute(self, args):
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

    def execute(self, args):
        try:
            manpage = Manpage(args[0])
            state = load_state()
            state["manpage"] = manpage.to_dict()
            save_state(state)
        except ManpageNotFoundException:
            sys.stderr.write(f"Could not find manpage `{args[0]}`.\n")


class Exit(Command):
    name = f"{SIGIL}exit"

    def execute(self, args):
        sys.exit(0)
