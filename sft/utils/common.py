""" This module contains common utilities, used all over the project.
"""


class Singleton(type):
    """ Use to create a singleton object.
    """

    def __init__(cls, name, bases, dict):
        super().__init__(name, bases, dict)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance


def run_once(func):
    "Decorator that runs a function only once and caches the result."
    def decorated(*args, **kwargs):
        try:
            return decorated._result
        except AttributeError:
            decorated._result = func(*args, **kwargs)
            return decorated._result
    return decorated
