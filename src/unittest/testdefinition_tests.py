__author__ = "Alexander Metzner"

import unittest
from pyassert import assert_that

from pyfix.decorators import GIVEN_ATTRIBUTE, BEFORE_ATTRIBUTE, AFTER_ATTRIBUTE
from pyfix.testdefinition import TestDefinition


class TestDefinitionTest(unittest.TestCase):
    def test_should_handle_givens(self):
        def some_function():
            pass

        givens = {"spam": "spam"}
        setattr(some_function, GIVEN_ATTRIBUTE, givens)

        test = TestDefinition.from_function(some_function)

        assert_that(test.givens).is_equal_to(givens)

    def test_should_construct_test_from_function_with_underscore_name(self):
        def some_function():
            "This is my description"

        test = TestDefinition.from_function(some_function)

        assert_that(test.function).is_identical_to(some_function)
        assert_that(test.name).is_equal_to("Some function")
        assert_that(test.description).is_equal_to("This is my description")
        assert_that(test.module).is_equal_to(__name__)

    def test_should_construct_test_from_function_with_camelcase_name(self):
        def someFunction():
            "This is my description"

        test = TestDefinition.from_function(someFunction)

        assert_that(test.function).is_identical_to(someFunction)
        assert_that(test.name).is_equal_to("Some function")
        assert_that(test.description).is_equal_to("This is my description")
        assert_that(test.module).is_equal_to(__name__)

    def test_should_collect_before_interceptors(self):
        def some_function():
            pass

        before_interceptors = ["spam", "eggs"]
        setattr(some_function, BEFORE_ATTRIBUTE, before_interceptors)

        test = TestDefinition.from_function(some_function)

        assert_that(test.before_interceptors).is_equal_to(before_interceptors)

    def test_should_collect_after_interceptors(self):
        def some_function():
            pass

        after_interceptors = ["spam", "eggs"]
        setattr(some_function, AFTER_ATTRIBUTE, after_interceptors)

        test = TestDefinition.from_function(some_function)

        assert_that(test.after_interceptors).is_equal_to(after_interceptors)
