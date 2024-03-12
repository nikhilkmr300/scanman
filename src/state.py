import json
import os


def save_state(state):
    dirpath = os.path.join(os.path.expanduser("~"), ".scanman")
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)

    with open(os.path.join(dirpath, "state.json"), "w") as f:
        json.dump(state, f)

def load_state():
    dirpath = os.path.join(os.path.expanduser("~"), ".scanman")
    with open(os.path.join(dirpath, "state.json"), "r") as f:
        return json.load(f)
