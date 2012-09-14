__author__ = "Alexander Metzner"

import unittest
from pyassert import assert_that

from pyfix.decorators import test, given, TEST_ATTRIBUTE, GIVEN_ATTRIBUTE

class TestDecoratorTest(unittest.TestCase):
    def test_should_mark_function_as_test (self):
        @test
        def some_test ():
            pass

        assert_that(hasattr(some_test, TEST_ATTRIBUTE)).is_true()

    def test_ensure_that_decorated_function_can_be_called (self):
        @test
        def some_test ():
            some_test.called = True

        some_test.called = False
        some_test()
        assert_that(some_test.called).is_true()


class GivenTest(unittest.TestCase):
    def test_should_raise_exception_when_no_arguments_are_given (self):
        try:
            @given()
            def some_function ():
                pass

            self.fail("ValueError expected")
        except ValueError as expected:
            pass

    def test_should_raise_exception_when_fixture_name_is_used_multiple_times (self):
        try:
            @given(spam="spam")
            @given(spam="eggs")
            def some_function ():
                pass

            self.fail("ValueError expected")
        except ValueError as expected:
            assert_that(str(expected)).equals(
                "Unable to define fixture with name 'spam' and value 'spam' because it is already given with value 'eggs'")
            pass

    def test_ensure_that_single_given_decorator_with_single_fixture_is_handled (self):
        @given(spam="spam")
        def some_function ():
            pass

        assert_that(getattr(some_function, GIVEN_ATTRIBUTE)).equals({"spam": "spam"})

    def test_ensure_that_single_given_decorator_with_multiple_fixtures_is_handled (self):
        @given(spam="spam", eggs="eggs")
        def some_function ():
            pass

        assert_that(getattr(some_function, GIVEN_ATTRIBUTE)).equals({"spam": "spam", "eggs": "eggs"})

    def test_ensure_that_single_two_decorators_with_multiple_fixtures_are_handled (self):
        @given(spam="spam", eggs="eggs")
        @given(foo="foo")
        def some_function ():
            pass

        assert_that(getattr(some_function, GIVEN_ATTRIBUTE)).equals({"spam": "spam", "eggs": "eggs", "foo": "foo"})

    def test_ensure_that_decorated_functions_can_be_executed (self):
        @given(spam="spam")
        def some_test ():
            some_test.called = True

        some_test.called = False
        some_test()
        assert_that(some_test.called).is_true()
