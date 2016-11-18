import cmd
from sft.client.commands import load_commands
from sft.common.sessions.session_manager import SessionManager


_session_manager = SessionManager()


def _create_command_instance(command_class, args_line):
    session = _session_manager.get_all_not_inactive_sessions()[0]
    session.command = command_class(args_line)


class CommandDispatcherBase(cmd.Cmd):
    """Base class for mapping app command names to command functionality.

       If you want to add a new command to app just add new method like
       do_<command_name>(self, line). Line contains string with command arguments.
       Note that command names are case-sensitive.
    """
    def __new__(cls, *args, **kwargs):
        for command in load_commands().values():
            alias = command.get_command_alias()
            if alias is not None:
                cmd_callable = lambda self, line: _create_command_instance(command, line)
                cmd_callable.__doc__ = command.__doc__
                setattr(cls, 'do_' + alias, cmd_callable)
        return super().__new__(cls, *args, **kwargs)

    def __init__(self):
        super().__init__()

    def emptyline(self):
        pass

    def do_exit(self, line):
        """Exit client."""
        raise KeyboardInterrupt
