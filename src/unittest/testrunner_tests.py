__author__ = "Alexander Metzner"

import unittest
from pyassert import assert_that
from mockito import mock, when, verify, any as any_value

from pyfix.testdefinition import TestDefinition
from pyfix.fixture import Fixture, enumerate
from pyfix.testrunner import TestRunner, TestRunListener, TestResult, TestSuiteResult, TestInjector

class TestRunnerNotificationTest(unittest.TestCase):
    def setUp (self):
        self.listener_mock = mock(TestRunListener)
        self.test_definition_mock = mock(TestDefinition)
        self.test_definition_mock.givens = {}
        self.suite = [self.test_definition_mock]

        self.injector_mock = mock(TestInjector)
        self.test_result_mock = mock(TestResult)
        when(self.injector_mock).execute_test(self.test_definition_mock).thenReturn([self.test_result_mock])

        self.test_runner = TestRunner()
        self.test_runner._injector = self.injector_mock
        self.test_runner.add_test_run_listener(self.listener_mock)

    def test_ensure_that_before_suite_is_called (self):
        self.test_runner.run_tests(self.suite)
        verify(self.listener_mock).before_suite(self.suite)

    def test_ensure_that_before_test_is_called (self):
        self.test_runner.run_tests(self.suite)
        verify(self.listener_mock).before_test(self.test_definition_mock)

    def test_ensure_that_after_test_is_called (self):
        self.test_runner.run_tests(self.suite)
        verify(self.listener_mock).after_test(any_value(list))

    def test_ensure_that_after_suite_is_called (self):
        self.test_runner.run_tests(self.suite)
        verify(self.listener_mock).after_suite(any_value(TestSuiteResult))


class TestRunnerExecutionTest(unittest.TestCase):
    def setUp(self):
        self.injector_mock = mock(TestInjector)

        self.test_runner = TestRunner()
        self.test_runner._injector = self.injector_mock

    def test_should_execute_test_function_when_running_test (self):
        test_definition_mock = mock(TestDefinition)
        when(self.injector_mock).execute_test(test_definition_mock).thenReturn(mock(TestResult))

        self.test_runner.run_test([test_definition_mock])

        when(self.injector_mock).execute_test(test_definition_mock)


class TestSuiteResultsTest (unittest.TestCase):
    def setUp (self):
        self.test_suite = TestSuiteResult()

    def test_should_return_success_when_no_test_has_been_recorded (self):
        assert_that(self.test_suite.success).is_true()

    def test_should_return_success_when_single_test_has_been_recorded (self):
        result = mock(TestResult)
        result.success = True
        self.test_suite.add_test_results([result])

        assert_that(self.test_suite.success).is_true()

    def test_should_return_no_success_when_single_test_with_failure_has_been_recorded (self):
        result = mock(TestResult)
        result.success = False
        self.test_suite.add_test_results([result])

        assert_that(self.test_suite.success).is_false()

    def test_should_count_number_of_tests_executed (self):
        failure = mock(TestResult)
        failure.success = False

        success = mock(TestResult)
        success.success = True

        self.test_suite.add_test_results([failure, success, success, failure])

        assert_that(self.test_suite.number_of_tests_executed).equals(4)

    def test_should_count_number_of_failures (self):
        failure = mock(TestResult)
        failure.success = False

        success = mock(TestResult)
        success.success = True

        self.test_suite.add_test_results([failure, success, success, failure])

        assert_that(self.test_suite.number_of_failures).equals(2)


class InvocationCountingFunctionMock (object):
    def __init__ (self, exception_to_raise=None):
        self._exception_to_raise = exception_to_raise
        self._invocation_arguments = []

    @property
    def invocation_counter (self):
        return len(self._invocation_arguments)

    @property
    def invocation_arguments (self):
        return self._invocation_arguments

    def __call__ (self, **arguments):
        self._invocation_arguments.append(arguments)
        if self._exception_to_raise is not None:
            raise self._exception_to_raise


class TestInjectorTest (unittest.TestCase):
    def setUp (self):
        self.injector = TestInjector()

    def test_ensure_that_test_is_marked_as_successful_when_being_executed_without_exception (self):
        function = InvocationCountingFunctionMock()
        test_definition = TestDefinition(function, "unittest", "unittest", "module", {})

        actual = self.injector.execute_test(test_definition)

        assert_that(actual[0].success).is_true()
        assert_that(actual[0].parameter_description).equals("")

    def test_ensure_that_test_is_marked_as_failing_when_being_executed_with_exception (self):
        function = InvocationCountingFunctionMock(AssertionError("Caboom"))
        test_definition = TestDefinition(function, "unittest", "unittest", "module", {})

        actual = self.injector.execute_test(test_definition)

        assert_that(actual[0].success).is_false()
        assert_that(actual[0].message).equals("Caboom")

    def test_should_invoke_test_function_once_when_no_givens_are_set (self):
        function = InvocationCountingFunctionMock()
        test_definition = TestDefinition(function, "unittest", "unittest", "module", {})

        self.injector.execute_test(test_definition)

        assert_that(function.invocation_counter).equals(1)
        assert_that(function.invocation_arguments[0]).equals({})

    def test_should_invoke_test_function_once_when_constant_given_is_set (self):
        function = InvocationCountingFunctionMock()
        test_definition = TestDefinition(function, "unittest", "unittest", "module", {"spam": "eggs"})

        result = self.injector.execute_test(test_definition)

        assert_that(function.invocation_counter).equals(1)
        assert_that(function.invocation_arguments[0]).equals({"spam": "eggs"})
        assert_that(result[0].parameter_description).equals("spam=eggs")

    def test_should_invoke_test_function_once_when_fixture_is_given_and_provide_and_reclaim_are_called (self):
        class TestFixture (Fixture):
            provide_invoked = False
            reclaim_invoked = False

            def provide(self):
                TestFixture.provide_invoked = True
                return ["spam"]

            def reclaim(self, value):
                TestFixture.reclaim_invoked = True
                assert_that(value).equals("spam")

        function = InvocationCountingFunctionMock()
        test_definition = TestDefinition(function, "unittest", "unittest", "module", {"spam": TestFixture})

        self.injector.execute_test(test_definition)

        assert_that(function.invocation_counter).equals(1)
        assert_that(function.invocation_arguments[0]).equals({"spam": "spam"})

        assert_that(TestFixture.provide_invoked).is_true()
        assert_that(TestFixture.reclaim_invoked).is_true()

    def test_should_invoke_test_function_twice_when_fixture_provides_two_values (self):
        function = InvocationCountingFunctionMock()
        test_definition = TestDefinition(function, "unittest", "unittest", "module", {"spam": enumerate("spam", "eggs")})

        self.injector.execute_test(test_definition)

        assert_that(function.invocation_counter).equals(2)

    def test_should_reclaim_all_values_when_fixture_returns_more_than_one_value (self):
        class TestFixture (Fixture):
            provide_invoked = 0
            reclaim_invoked = 0

            def provide(self):
                TestFixture.provide_invoked += 1
                return ["spam", "eggs"]

            def reclaim(self, value):
                TestFixture.reclaim_invoked += 1

        function = InvocationCountingFunctionMock()
        test_definition = TestDefinition(function, "unittest", "unittest", "module", {"spam": TestFixture})

        self.injector.execute_test(test_definition)

        assert_that(TestFixture.provide_invoked).equals(1)
        assert_that(TestFixture.reclaim_invoked).equals(2)

    def test_should_invoke_test_function_four_times_when_two_fixtures_each_provide_two_values (self):
        function = InvocationCountingFunctionMock()
        test_definition = TestDefinition(function, "unittest", "unittest", "module",
                {"spam": enumerate("spam", "eggs"),
                 "foo": enumerate("foo", "bar")})

        self.injector.execute_test(test_definition)

        assert_that(function.invocation_counter).equals(4)
        assert_that(function.invocation_arguments).contains({"spam": "spam", "foo": "foo"})
        assert_that(function.invocation_arguments).contains({"spam": "spam", "foo": "bar"})
        assert_that(function.invocation_arguments).contains({"spam": "eggs", "foo": "foo"})
        assert_that(function.invocation_arguments).contains({"spam": "eggs", "foo": "bar"})
