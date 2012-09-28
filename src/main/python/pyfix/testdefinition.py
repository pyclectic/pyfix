#  pyfix
#  Copyright 2012 The pyfix team.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

__author__ = "Alexander Metzner"

from .utils import humanize_camel_case_name, humanize_underscore_name
from .decorators import GIVEN_ATTRIBUTE, BEFORE_ATTRIBUTE, AFTER_ATTRIBUTE

class TestDefinition(object):
    @classmethod
    def from_function(cls, function):
        name = function.__name__
        if "_" in name:
            name = humanize_underscore_name(name)
        else:
            name = humanize_camel_case_name(name)

        description = function.__doc__

        givens = {}
        if hasattr(function, GIVEN_ATTRIBUTE):
            givens = getattr(function, GIVEN_ATTRIBUTE)

        before = []
        if hasattr(function, BEFORE_ATTRIBUTE):
            before = getattr(function, BEFORE_ATTRIBUTE)

        after = []
        if hasattr(function, AFTER_ATTRIBUTE):
            after = getattr(function, AFTER_ATTRIBUTE)

        return cls(function, name, description, function.__module__, givens, before, after)

    def __init__(self, function, name, description, module, givens, before_interceptors=None, after_interceptors=None):
        self.function = function
        self.name = name
        self.description = description
        self.module = module
        self.givens = givens
        self.before_interceptors = before_interceptors if before_interceptors is not None else []
        self.after_interceptors = after_interceptors if after_interceptors is not None else []
