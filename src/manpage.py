import json
import subprocess
import sys


class Manpage:
    def __init__(self, name):
        self.name = name
        self._validate()

    def content(self):
        return subprocess.run(f"man {self.name}", capture_output=True, shell=True, check=True)

    def _validate(self):
        try:
            self.content()
        except subprocess.CalledProcessError:
            raise ManpageNotFoundException(f"Could not find manpage `{self.name}`")

    def to_dict(self):
        return {"name": self.name}

    @classmethod
    def from_dict(cls, data):
        if data:
            return cls(**data)
        return None

class ManpageNotFoundException(Exception):
    pass
