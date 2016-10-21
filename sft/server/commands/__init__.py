from sft.utils.common import import_submodules
from sft.server.commands.base import CommandBase

def import_commands():
    submodules = import_submodules(__name__).keys()
    for module in submodules:
        for item in module.__all__:
            if issubclass(item, CommandBase):
                globals().
    print(submodules)


import_commands()
