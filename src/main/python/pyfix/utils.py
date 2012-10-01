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

"""
Provides some utility functions and classes.
"""

__author__ = "Alexander Metzner"

import types

def humanize_underscore_name(function_name):
    if "_" in function_name:
        return function_name.replace("_", " ").capitalize()
    return function_name


def humanize_camel_case_name(function_name):
    if "_" in function_name:
        return function_name
    return _de_camel_case(function_name)


def _de_camel_case(name):
    result = ""
    for char in name:
        if char.isupper():
            result += " " + char.lower()
        else:
            result += char
    if result[0] == " ":
        result = result[1:]
    return result.capitalize()
