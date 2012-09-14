__author__ = "Alexander Metzner"

import unittest
from pyassert import assert_that
from mockito import mock, when, verify, any as any_value

from pyfix.testdefinition import TestDefinition
from pyfix.testrunner import TestRunner, TestRunListener, TestResult, TestSuiteResult

class TestRunnerNotificationTest(unittest.TestCase):
    def setUp (self):
        self.test_runner = TestRunner()
        self.listener_mock = mock(TestRunListener)
        self.test_definition_mock = mock(TestDefinition)
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
