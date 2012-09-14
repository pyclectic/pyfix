__author__ = "Alexander Metzner"

import unittest
from pyassert import assert_that
from mockito import mock, when, verify, any as any_value

from pyfix.testdefinition import TestDefinition
from pyfix.fixture import Fixture
from pyfix.testrunner import TestRunner, TestRunListener, TestResult, TestSuiteResult, TestExecutionInjector

class TestRunnerNotificationTest(unittest.TestCase):
    def setUp (self):
        self.test_runner = TestRunner()
        self.listener_mock = mock(TestRunListener)
        self.test_definition_mock = mock(TestDefinition)
        self.test_definition_mock.givens = {}
        self.test_runner.add_test_run_listener(self.listener_mock)
        self.suite = [self.test_definition_mock]

    def test_ensure_that_before_suite_is_called (self):
        self.test_runner.run_tests(self.suite)
        verify(self.listener_mock).before_suite(self.suite)

    def test_ensure_that_before_test_is_called (self):
        self.test_runner.run_tests(self.suite)
        verify(self.listener_mock).before_test(self.test_definition_mock)

    def test_ensure_that_after_test_is_called (self):
        self.test_runner.run_tests(self.suite)
        verify(self.listener_mock).after_test(any_value(TestResult))

    def test_ensure_that_after_suite_is_called (self):
        self.test_runner.run_tests(self.suite)
        verify(self.listener_mock).after_suite(any_value(TestSuiteResult))


class TestRunnerExecutionTest(unittest.TestCase):
    def setUp(self):
        self.test_runner = TestRunner()

    def test_should_execute_test_function_when_running_test (self):
        def test ():
            test.executed = True
        test.executed = False

        self.test_runner.run_test(TestDefinition.from_function(test))

        assert_that(test.executed).is_true()

    def test_ensure_that_execution_is_marked_as_successful_when_test_terminated_normally (self):
        def test ():
            pass
        test_result = self.test_runner.run_test(TestDefinition.from_function(test))

        assert_that(test_result.success).is_true()

    def test_ensure_that_execution_is_marked_as_failed_when_test_terminated_normally (self):
        def test ():
            raise Exception("caboom")
        test_result = self.test_runner.run_test(TestDefinition.from_function(test))

        assert_that(test_result.success).is_false()

    def test_ensure_that_non_negative_time_is_recorded_for_test (self):
        def test ():
            pass
        test_result = self.test_runner.run_test(TestDefinition.from_function(test))

        assert_that(test_result.execution_time).equals(0)


class TestSuiteResultsTest (unittest.TestCase):
    def setUp (self):
        self.test_suite = TestSuiteResult()

    def test_should_return_success_when_no_test_has_been_recorded (self):
        assert_that(self.test_suite.success).is_true()

    def test_should_return_success_when_single_test_has_been_recorded (self):
        result = mock(TestResult)
        result.success = True
        self.test_suite.add_test_result(result)

        assert_that(self.test_suite.success).is_true()

    def test_should_return_no_success_when_single_test_with_failure_has_been_recorded (self):
        result = mock(TestResult)
        result.success = False
        self.test_suite.add_test_result(result)

        assert_that(self.test_suite.success).is_false()

    def test_should_count_number_of_tests_executed (self):
        failure = mock(TestResult)
        failure.success = False

        success = mock(TestResult)
        success.success = True

        self.test_suite.add_test_result(failure)
        self.test_suite.add_test_result(success)
        self.test_suite.add_test_result(success)
        self.test_suite.add_test_result(failure)

        assert_that(self.test_suite.number_of_tests_executed).equals(4)

    def test_should_count_number_of_failures (self):
        failure = mock(TestResult)
        failure.success = False

        success = mock(TestResult)
        success.success = True

        self.test_suite.add_test_result(failure)
        self.test_suite.add_test_result(success)
        self.test_suite.add_test_result(success)
        self.test_suite.add_test_result(failure)

        assert_that(self.test_suite.number_of_failures).equals(2)



class TestExecutionInjectorTest (unittest.TestCase):
    def setUp (self):
        self.injector = TestExecutionInjector()

    def test_should_return_object_when_given_value_is_object (self):
        value = "spam"
        assert_that(self.injector.resolve_parameter_value(value)).is_identical_to(value)

    def test_should_return_instance_when_given_value_is_class (self):
        class Spam:
            pass
        assert_that(isinstance(self.injector.resolve_parameter_value(Spam), Spam)).is_true()

    def test_should_return_provided_value_when_given_value_is_fixture_class (self):
        class Spam (Fixture):
            def provide (self):
                return "eggs"

        assert_that(self.injector.resolve_parameter_value(Spam)).equals("eggs")

    def test_should_inject_parameters (self):
        class Spam (Fixture):
            def provide (self):
                return "eggs"

        test_definition = mock(TestDefinition)
        test_definition.givens = {"spam": "spam", "eggs": Spam}

        assert_that(self.injector.provide_parameters(test_definition)).equals([{"spam": "spam", "eggs": "eggs"}])


    def test_ensure_that_fixture_value_is_reclaimed_when_test_finishes (self):
        class TestFixture (Fixture):
            executed = False
            def reclaim (self, value):
                assert_that(value).equals("spam")
                TestFixture.executed = True

            def provide (self):
                return "spam"

        test_definition = mock(TestDefinition)
        test_definition.givens = {"spam": TestFixture}

        parameters = self.injector.provide_parameters(test_definition)
        self.injector.reclaim_parameters(test_definition, parameters)

        assert_that(TestFixture.executed).is_true()
