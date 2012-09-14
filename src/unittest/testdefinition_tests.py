__author__ = "Alexander Metzner"

import unittest
from pyassert import assert_that

from pyfix.decorators import GIVEN_ATTRIBUTE
from pyfix.testdefinition import TestDefinition


class TestTest(unittest.TestCase):
    def test_should_handle_givens (self):
        def some_function ():
            pass

        givens = {"spam": "spam"}
        setattr(some_function, GIVEN_ATTRIBUTE, givens)

        test = TestDefinition.from_function(some_function)

        assert_that(test.givens).equals(givens)

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

