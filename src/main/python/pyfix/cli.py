"""
This module provides classes and functions that make up the command line interface of pyfix.
"""

from __future__ import print_function

__author__ = "Alexander Metzner"

import sys

from pyfix import __version__
from .testcollector import TestCollector
from .testrunner import TestRunListener, TestRunner

def red (message):
    if sys.stdout.isatty():
        return "\033[31m%s\033[0;0m" % message
    return message


def green (message):
    if sys.stdout.isatty():
        return "\033[32m%s\033[0;0m" % message
    return message


class TtyTestRunListener(TestRunListener):
    def before_test (self, test_definition):
        sys.stdout.write("{0}: ".format(test_definition.name))
        sys.stdout.flush()

    def after_test (self, test_result):
        if test_result.success:
            sys.stdout.write(green("passed"))
        else:
            sys.stdout.write(red("failed"))
        sys.stdout.write(" [{0:d} ms] ({1:d} run{2})".format(test_result.execution_time, test_result.number_of_runs,
            "s" if test_result.number_of_runs != 1 else ""))
        if not test_result.success:
            sys.stdout.write("\n\t{0}".format(test_result.message))
        sys.stdout.write("\n")

    def before_suite (self, test_definitions):
        number_of_tests = len(test_definitions)
        print("Running {0} test{1}.".format(number_of_tests, "s" if number_of_tests else ""))
        self._hr()

    def after_suite (self, test_results):
        self._hr()
        print("TEST RESULTS SUMMARY")
        print("\t{0:3d} tests executed in {1:d} ms".format(test_results.number_of_tests_executed,
            test_results.execution_time))
        print("\t{0:3d} tests failed".format(test_results.number_of_failures))

    def _hr (self):
        print("-" * 80)


def banner ():
    print("pyfix version {0}.".format(__version__))
    print()


def run_tests ():
    """
    Main cli function. Executes all tests defined in the __main__ module and issues all reports to STDOUT using
    tty coloring if supported by STDOUT.
    """
    banner()

    import __main__

    collector = TestCollector()
    collector.collect_tests(__main__)

    runner = TestRunner()
    runner.add_test_run_listener(TtyTestRunListener())
    test_suite_result = runner.run_tests(collector.test_suite)

    if test_suite_result.success:
        print(green("ALL TESTS PASSED"))
    else:
        print(red("THERE WERE TEST FAILURES"))
        sys.exit(1)
