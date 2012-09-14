__author__ = "Alexander Metzner"

from .utils import humanize_camel_case_name, humanize_underscore_name

class TestDefinition(object):
    @classmethod
    def from_function (cls, function):
        name = function.__name__
        if "_" in name:
            name = humanize_underscore_name(name)
        else:
            name = humanize_camel_case_name(name)

        description = function.__doc__

        return cls(function, name, description, function.__module__)

    def __init__ (self, function, name, description, module):
        self.function = function
        self.name = name
        self.description = description
        self.module = module

