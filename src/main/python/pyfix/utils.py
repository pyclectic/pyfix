"""
Provides some utility functions and classes.
"""

__author__ = "Alexander Metzner"

def humanize_underscore_name (function_name):
    if "_" in function_name:
        return function_name.replace("_", " ").capitalize()
    return function_name


def humanize_camel_case_name (function_name):
    if "_" in function_name:
        return function_name
    return _de_camel_case(function_name)


def _de_camel_case (name):
    result = ""
    for char in name:
        if char.isupper():
            result += " " + char.lower()
        else:
            result += char
    if result[0] == " ":
        result = result[1:]
    return result.capitalize()

