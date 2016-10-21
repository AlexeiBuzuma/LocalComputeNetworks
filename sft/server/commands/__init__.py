import logging

from sft.utils.common import import_submodules, run_once
from sft.server.commands.base import CommandBase


LOG = logging.getLogger(__name__)


@run_once
def load_commands():
    commands = {}
    submodules = import_submodules(__name__).values()
    for module in submodules:
        try:
            for attr_name in module.__all__:
                attr = getattr(module, attr_name)
                if issubclass(attr, CommandBase):
                    commands[attr_name] = attr
        except AttributeError as e:
            pass
    globals().update(commands)
    LOG.debug('Loaded commands: %r', list(commands.keys()))


load_commands()
