__author__ = "Alexander Metzner"

import inspect
import sys
import time

from .fixture import Fixture

class TestRunListener(object):
    def before_suite (self, test_definitions):
        pass

    def before_test (self, test_definition):
        pass

    def after_test (self, test_result):
        pass

    def after_suite (self, test_results):
        pass


class TestResult(object):
    def __init__ (self, test_definition, success, execution_time, message = None):
        self.test_definition = test_definition
        self.success = success
        self.execution_time = execution_time
        self.message = message


class TestSuiteResult(object):
    def __init__ (self):
        self.test_results = []
        self.execution_time = -1

    def add_test_result (self, test_result):
        self.test_results.append(test_result)

    @property
    def number_of_tests_executed (self):
        return len(self.test_results)

    @property
    def number_of_failures (self):
        return len([r for r in self.test_results if not r.success])

    @property
    def success (self):
        for test_result in self.test_results:
            if not test_result.success:
                return False
        return True


class TestExecutionInjector (object):
    def provide_parameters (self, test_definition):
        parameters = {}

        for given in test_definition.givens:
            parameters[given] = self.resolve_parameter_value(test_definition.givens[given])

        return parameters

    def reclaim_parameters (self, test_definition, parameters):
        for given in test_definition.givens:
            self.reclaim_parameter_value(test_definition.givens[given], parameters[given])

    def reclaim_parameter_value (self, given_value, parameter_value):
        if inspect.isclass(given_value):
            given_value = given_value()

        if isinstance(given_value, Fixture):
            given_value.reclaim(parameter_value)

    def resolve_parameter_value (self, given_value):
        if inspect.isclass(given_value):
            given_value = given_value()

        if isinstance(given_value, Fixture):
            given_value = given_value.provide()

        return given_value


class TestRunner(object):
    def __init__ (self):
        self._injector = TestExecutionInjector()
        self._listeners = []

    def add_test_run_listener (self, test_run_listener):
        self._listeners.append(test_run_listener)

    def run_tests (self, test_definitions):
        test_suite_result = TestSuiteResult()
        self._notify_listeners(lambda l: l.before_suite(test_definitions))

        start = time.time()

        for test_definition in test_definitions:
            test_suite_result.add_test_result(self.run_test(test_definition))

        end = time.time()
        test_suite_result.execution_time = int((end - start) / 1000)

        self._notify_listeners(lambda l: l.after_suite(test_suite_result))

        return test_suite_result

    def run_test (self, test_definition):
        self._notify_listeners(lambda l: l.before_test(test_definition))

        start = time.time()

        message = None
        success = True

        parameters = self._injector.provide_parameters(test_definition)
        try:
            test_definition.function(**parameters)
        except:
            message = sys.exc_info()[1]
            success = False
        finally:
            self._injector.reclaim_parameters(test_definition, parameters)

        end = time.time()
        test_result = TestResult(test_definition, success, int((end - start) / 1000), message)

        self._notify_listeners(lambda l: l.after_test(test_result))
        return test_result


    def _notify_listeners (self, callback):
        for listener in self._listeners:
            callback(listener)