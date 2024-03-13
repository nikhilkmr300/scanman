import json
import subprocess
import sys


class Manpage:
    def __init__(self, name):
        self.name = name
        self._validate()

    def content(self):
        return subprocess.run(f"man {self.name}", capture_output=True, shell=True, check=True).stdout.decode("utf-8")

    def _validate(self):
        try:
            self.content()
        except subprocess.CalledProcessError:
            raise ManpageNotFoundException(f"Could not find manpage `{self.name}`")

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name})"


class ManpageNotFoundException(Exception):
    pass
