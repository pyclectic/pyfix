__author__ = "Alexander Metzner"

import copy
import inspect
import sys
import time
import traceback

from .fixture import Fixture, ConstantFixture

class TestRunListener(object):
    """
    Interface class for listeners that can be registered with a TestRunner to receive notifications about events
    that occurred during execution of tests.
    """

    def before_suite(self, test_definitions):
        "Called before the execution of the test suite starts. Receives the list of all TestDefinitions to execute."
        pass

    def before_test(self, test_definition):
        "Called before the given TestDefinition is executed."
        pass

    def after_test(self, test_results):
        """
        Called after a single test definition has been executed. As a single test definition can spawn several test
        executions a list of TestResults is passed in.
        """
        pass

    def after_suite(self, test_suite_result):
        "Called after the suite has been executed. The TestSuiteResult is passed in."
        pass


class TestResult(object):
    "The result of a single test execution."

    def __init__(self, test_definition, success, execution_time, parameter_description, message, traceback):
        """
        test_definition -- the TestDefinition that has been executed
        success -- True if the execution was successfull, False otherwise
        execution_time -- Time in milli seconds it took to execute the test
        parameter_description -- String that describes the parameter that have been used for this execution
        message -- Message describing the failure
        traceback -- Traceback in case of a failure or None
        """
        self.test_definition = test_definition
        self.success = success
        self.execution_time = execution_time
        self.parameter_description = parameter_description
        self.message = message
        self.traceback = traceback

    @property
    def traceback_as_string(self):
        return "\n".join(traceback.format_tb(self.traceback))


class TestSuiteResult(object):
    "The result of an execution of a test suite a.k.a. a list of test definitions."

    def __init__(self):
        self.test_results = []
        self.execution_time = -1

    def add_test_results(self, test_results):
        self.test_results += [r for r in test_results]

    @property
    def number_of_tests_executed(self):
        return len(self.test_results)

    @property
    def number_of_failures(self):
        return len([r for r in self.test_results if not r.success])

    @property
    def success(self):
        for test_result in self.test_results:
            if not test_result.success:
                return False
        return True


class TestInjector(object):
    """
    Instances of this class are used to calculate parameter values from TestDefinitions and execute the test function
    with the respective arguments.
    """

    def execute_test(self, test_definition):
        "Executes the given TestDefinition and returns a list of TestResults; one result for each execution."
        results = []

        fixtures = self._resolve_fixtures(test_definition)

        parameter_sets = self._multiply_parameter_maps(fixtures)

        for parameters in parameter_sets:
            results.append(self._execute_test_once(test_definition, fixtures, parameters))

        for name, (fixture, values) in fixtures.items():
            for value in values:
                fixture.reclaim(value)

        return results

    def _multiply_parameter_maps(self, fixtures):
        results = None

        for name, (fixture, values) in fixtures.items():
            if results is None:
                results = []
                for value in values:
                    results.append({name: value})
            else:
                new_results = []
                for result in results:
                    for value in values:
                        result = copy.deepcopy(result)
                        result[name] = value
                        new_results.append(result)
                results = new_results

        if results is None:
            results = [{}]
        return results

    def _resolve_fixtures(self, test_definition):
        result = {}
        for name, value in test_definition.givens.items():
            result[name] = self._resolve_fixture_and_values(value)
        return result

    def _resolve_fixture_and_values(self, given_value):
        if inspect.isclass(given_value):
            given_value = given_value()

        if not isinstance(given_value, Fixture):
            given_value = ConstantFixture(given_value)

        return (given_value, given_value.provide())


    def _get_exception_information(self):
        exception_information = sys.exc_info()
        type_name = exception_information[0].__name__
        value = str(exception_information[1])
        return type_name + ": " + value, exception_information[2]

    def _execute_interceptors(self, interceptors):
        for interceptor in interceptors:
            interceptor()

    def _execute_test_once(self, test_definition, fixtures, parameters):
        start = time.time()

        message = None
        traceback = None
        success = False

        try:
            self._execute_interceptors(test_definition.before_interceptors)

            try:
                test_definition.function(**parameters)
                success = True
            except AssertionError as error:
                message = str(error)
            except:
                message, traceback = self._get_exception_information()

        except:
            message, traceback = self._get_exception_information()
            message = "Execution of before interceptor failed: " + message
            success = False

        finally:
            try:
                self._execute_interceptors(test_definition.after_interceptors)
            except:
                message, traceback = self._get_exception_information()
                message = "Execution of after interceptor failed: " + message
                success = False

        end = time.time()

        return TestResult(test_definition, success, int((end - start) * 1000),
            self._build_parameter_description(fixtures, parameters), message, traceback)

    def _build_parameter_description(self, fixtures, parameters):
        result_list = []
        for name in sorted(fixtures.keys()):
            result_list.append("{0}={1}".format(name, fixtures[name][0].describe(parameters[name])))

        return " ".join(result_list)


class TestRunner(object):
    """
    Runner that executes tests and test suites.

    Multiple TestRunListener can be registered with a test runner to receive notifications about events during
    execution.
    """

    def __init__(self):
        self._injector = TestInjector()
        self._listeners = []

    def add_test_run_listener(self, test_run_listener):
        "Registers the given TestRunListener."
        self._listeners.append(test_run_listener)

    def run_tests(self, test_definitions):
        "Executes all given TestDefinitions and returns a TestSuiteResult."
        test_suite_result = TestSuiteResult()
        self._notify_listeners(lambda l: l.before_suite(test_definitions))

        start = time.time()

        for test_definition in test_definitions:
            test_suite_result.add_test_results(self.run_test(test_definition))

        end = time.time()
        test_suite_result.execution_time = int((end - start) * 1000)

        self._notify_listeners(lambda l: l.after_suite(test_suite_result))

        return test_suite_result

    def run_test(self, test_definition):
        "Executes a single TestDefinition and returns a list of TestResults."
        self._notify_listeners(lambda l: l.before_test(test_definition))

        test_results = self._injector.execute_test(test_definition)

        self._notify_listeners(lambda l: l.after_test(test_results))
        return test_results


    def _notify_listeners(self, callback):
        for listener in self._listeners:
            callback(listener)
