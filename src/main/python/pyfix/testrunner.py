__author__ = "Alexander Metzner"

import copy
import inspect
import sys
import time

from .fixture import Fixture, ConstantFixture

class TestRunListener(object):
    def before_suite(self, test_definitions):
        pass

    def before_test(self, test_definition):
        pass

    def after_test(self, test_results):
        pass

    def after_suite(self, test_results):
        pass


class TestResult(object):
    def __init__(self, test_definition, success, execution_time, message, parameter_description):
        self.test_definition = test_definition
        self.success = success
        self.execution_time = execution_time
        self.message = message
        self.parameter_description = parameter_description


class TestSuiteResult(object):
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
    def execute_test(self, test_definition):
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

    def _execute_test_once(self, test_definition, fixtures, parameters):
        start = time.time()

        message = None
        success = True

        try:
            test_definition.function(**parameters)
        except:
            message = str(sys.exc_info()[1])
            success = False

        end = time.time()

        return TestResult(test_definition, success, int((end - start) * 1000), message,
            self._build_parameter_description(fixtures, parameters))

    def _build_parameter_description (self, fixtures, parameters):
        result_list = []
        for name in sorted(fixtures.keys()):
            result_list.append("{0}={1}".format(name, fixtures[name][0].describe(parameters[name])))

        return " ".join(result_list)


class TestRunner(object):
    def __init__(self):
        self._injector = TestInjector()
        self._listeners = []

    def add_test_run_listener(self, test_run_listener):
        self._listeners.append(test_run_listener)

    def run_tests(self, test_definitions):
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
        self._notify_listeners(lambda l: l.before_test(test_definition))

        test_results = self._injector.execute_test(test_definition)

        self._notify_listeners(lambda l: l.after_test(test_results))
        return test_results


    def _notify_listeners(self, callback):
        for listener in self._listeners:
            callback(listener)
