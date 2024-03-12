from termcolor import colored

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
