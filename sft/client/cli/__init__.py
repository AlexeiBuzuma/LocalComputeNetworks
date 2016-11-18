_is_cli_input_disabled = False


def is_cli_input_disabled():
    return _is_cli_input_disabled


def disable_cli_input():
    global _is_cli_input_disabled
    _is_cli_input_disabled = True


def enable_cli_input():
    global _is_cli_input_disabled
    _is_cli_input_disabled = False
