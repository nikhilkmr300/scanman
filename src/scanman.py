#! /usr/bin/env python3

import readline

from commands import Command
from manpage import Manpage
from state import load_state, save_state
from cli import prompt

if __name__ == "__main__":
    state = {"manpage": None}
    save_state(state)

    while True:
        state = load_state()
        manpage = Manpage.from_dict(state["manpage"])

        input_ = prompt(manpage=manpage).split(" ")

        if Command.is_command(input_[0]):
            cmd_name, cmd_args = input_[0], input_[1:]
            cmd = Command.parse(cmd_name)
            cmd.execute(cmd_args)

        else:
            print("<LLMOutput>")
