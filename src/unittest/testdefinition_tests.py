__author__ = "Alexander Metzner"

import unittest
from pyassert import assert_that

from pyfix.testdefinition import TestDefinition

class TestTest(unittest.TestCase):
    def test_should_construct_test_from_function_with_underscore_name (self):
        def some_function ():
            "This is my description"

        test = TestDefinition.from_function(some_function)

        assert_that(test.function).is_identical_to(some_function)
        assert_that(test.name).equals("Some function")
        assert_that(test.description).equals("This is my description")
        assert_that(test.module).equals(__name__)

    def test_should_construct_test_from_function_with_camelcase_name (self):
        def someFunction ():
            "This is my description"

        test = TestDefinition.from_function(someFunction)

        assert_that(test.function).is_identical_to(someFunction)
        assert_that(test.name).equals("Some function")
        assert_that(test.description).equals("This is my description")
        assert_that(test.module).equals(__name__)

