__author__ = "Alexander Metzner"

import unittest
from pyassert import assert_that

from pyfix.decorators import (test, given, before, after, TEST_ATTRIBUTE, GIVEN_ATTRIBUTE, BEFORE_ATTRIBUTE,
                              AFTER_ATTRIBUTE)

class TestDecoratorTest(unittest.TestCase):
    def test_should_mark_function_as_test(self):
        @test
        def some_test():
            pass

        assert_that(hasattr(some_test, TEST_ATTRIBUTE)).is_true()

    def test_ensure_that_decorated_function_can_be_called(self):
        @test
        def some_test():
            some_test.called = True

        some_test.called = False
        some_test()
        assert_that(some_test.called).is_true()


class GivenTest(unittest.TestCase):
    def test_should_raise_exception_when_no_arguments_are_given(self):
        try:
            @given()
            def some_function():
                pass

            self.fail("ValueError expected")
        except ValueError as expected:
            pass

    def test_should_raise_exception_when_fixture_name_is_used_multiple_times(self):
        try:
            @given(spam="spam")
            @given(spam="eggs")
            def some_function():
                pass

            self.fail("ValueError expected")
        except ValueError as expected:
            assert_that(str(expected)).equals(
                "Unable to define fixture with name 'spam' and value 'spam' because it is already given with value 'eggs'")
            pass

    def test_ensure_that_single_given_decorator_with_single_fixture_is_handled(self):
        @given(spam="spam")
        def some_function():
            pass

        assert_that(getattr(some_function, GIVEN_ATTRIBUTE)).equals({"spam": "spam"})

    def test_ensure_that_single_given_decorator_with_multiple_fixtures_is_handled(self):
        @given(spam="spam", eggs="eggs")
        def some_function():
            pass

        assert_that(getattr(some_function, GIVEN_ATTRIBUTE)).equals({"spam": "spam", "eggs": "eggs"})

    def test_ensure_that_single_two_decorators_with_multiple_fixtures_are_handled(self):
        @given(spam="spam", eggs="eggs")
        @given(foo="foo")
        def some_function():
            pass

        assert_that(getattr(some_function, GIVEN_ATTRIBUTE)).equals({"spam": "spam", "eggs": "eggs", "foo": "foo"})

    def test_ensure_that_decorated_functions_can_be_executed(self):
        @given(spam="spam")
        def some_test():
            some_test.called = True

        some_test.called = False
        some_test()
        assert_that(some_test.called).is_true()


class BeforeTest(unittest.TestCase):
    def test_should_register_interceptor(self):
        def some_interceptor(): pass

        @before(some_interceptor)
        def some_test(): pass

        assert_that(getattr(some_test, BEFORE_ATTRIBUTE)).is_equal_to([some_interceptor])

    def test_should_register_multiple_interceptors(self):
        def some_interceptor(): pass

        def some_other_interceptor(): pass

        @before(some_interceptor)
        @before(some_other_interceptor)
        def some_test(): pass

        assert_that(getattr(some_test, BEFORE_ATTRIBUTE)).is_equal_to([some_interceptor, some_other_interceptor])

    def test_should_raise_exception_when_trying_to_register_non_callable(self):
        def callback():
            @before("spam")
            def spam(): pass

        self.assertRaises(ValueError, callback)


class AfterTest(unittest.TestCase):
    def test_should_register_interceptor(self):
        def some_interceptor(): pass

        @after(some_interceptor)
        def some_test(): pass

        assert_that(getattr(some_test, AFTER_ATTRIBUTE)).is_equal_to([some_interceptor])

    def test_should_register_multiple_interceptors(self):
        def some_interceptor(): pass

        def some_other_interceptor(): pass

        @after(some_interceptor)
        @after(some_other_interceptor)
        def some_test(): pass

        assert_that(getattr(some_test, AFTER_ATTRIBUTE)).is_equal_to([some_interceptor, some_other_interceptor])

    def test_should_raise_exception_when_trying_to_register_non_callable(self):
        def callback():
            @after("spam")
            def spam(): pass

        self.assertRaises(ValueError, callback)
