""" This module contains common utilities, used all over the project.
"""
import sys
import pkgutil
import importlib


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


def import_submodules(package_name):
    """ Import all submodules of a module, recursively

    :param package_name: Package name
    :type package_name: str
    :rtype: dict[types.ModuleType]
    """
    package = sys.modules[package_name]
    return {
        name: importlib.import_module(package_name + '.' + name)
        for loader, name, is_pkg in pkgutil.walk_packages(package.__path__)
    }
