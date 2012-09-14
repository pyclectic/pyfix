__author__ = "Alexander Metzner"

from .decorators import TEST_ATTRIBUTE
from .testdefinition import TestDefinition

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
