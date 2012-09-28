#  pyfix
#  Copyright 2012 The pyfix team.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""
This module provides classes and functions that make up the command line interface of pyfix.
"""

from __future__ import print_function

__author__ = "Alexander Metzner"

import sys

from pyfix import __version__
from .testcollector import TestCollector
from .testrunner import TestRunListener, TestRunner

def red(message):
    if sys.stdout.isatty():
        return "\033[31m%s\033[0;0m" % message
    return message


def green(message):
    if sys.stdout.isatty():
        return "\033[32m%s\033[0;0m" % message
    return message


def bold(message):
    if sys.stdout.isatty():
        return "\033[1m%s\033[0;0m" % message
    return message


class TtyTestRunListener(TestRunListener):
    def __init__ (self):
        self._test_written = False

    def before_test(self, test_definition):
        if self._test_written:
            self._hr()

        sys.stdout.write("{0}: ".format(bold(test_definition.name)))
        sys.stdout.flush()

    def after_test(self, test_results):
        for test_result in test_results:
            self._test_written = True
            sys.stdout.write("\n\t")
            if test_result.parameter_description:
                sys.stdout.write("{0}: ".format(test_result.parameter_description))
            if test_result.success:
                sys.stdout.write(green("passed"))
            else:
                sys.stdout.write(red("failed"))
            sys.stdout.write(" [{0:d} ms]".format(test_result.execution_time))
            if not test_result.success:
                sys.stdout.write(" {0}".format(test_result.message))
            if test_result.traceback:
                sys.stdout.write("\n{0}".format(test_result.traceback_as_string))
        sys.stdout.write("\n")


    def before_suite(self, test_definitions):
        number_of_tests = len(test_definitions)
        print("Running {0} test{1}.".format(number_of_tests, "s" if number_of_tests else ""))
        self._bold_hr()

    def after_suite(self, test_suite_result):
        self._bold_hr()
        print("TEST RESULTS SUMMARY")
        print("\t{0:3d} tests executed in {1:d} ms".format(test_suite_result.number_of_tests_executed,
            test_suite_result.execution_time))
        print("\t{0:3d} tests failed".format(test_suite_result.number_of_failures))

    def _bold_hr(self):
        print("=" * 80)

    def _hr(self):
        print("-" * 80)


def banner():
    print("pyfix version {0}.".format(__version__))
    print()


def run_tests():
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
