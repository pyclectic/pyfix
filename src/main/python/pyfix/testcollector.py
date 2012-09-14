__author__ = "Alexander Metzner"

from .testdefinition import TestDefinition

TEST_ATTRIBUTE = "PYFIX_TEST"

def test (function):
    setattr(function, TEST_ATTRIBUTE, True)
    return function


class TestCollector(object):
    def __init__ (self):
        self._tests = []

    @property
    def test_suite (self):
        return self._tests

    def collect_tests (self, module):
        for name in dir(module):
            candidate = getattr(module, name)
            if hasattr(candidate, TEST_ATTRIBUTE):
                self.register_test(candidate)

    def register_test (self, function):
        self._tests.append(TestDefinition.from_function(function))
