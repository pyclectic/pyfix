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

__author__ = "Alexander Metzner"

import unittest
from mockito import mock
from pyassert import assert_that

from pyfix.decorators import test
from pyfix.testcollector import TestCollector

class TestCollectorTest(unittest.TestCase):
    def setUp (self):
        self.collector = TestCollector()

    def test_should_collect_single_test_from_module (self):
        @test
        def some_test ():
            pass

        module_mock = mock()
        module_mock.some_test = some_test

        self.collector.collect_tests(module_mock)

        assert_that(len(self.collector.test_suite)).equals(1)

    def test_should_not_collect_method_not_marked_as_test (self):
        def some_test ():
            pass

        module_mock = mock()
        module_mock.some_test = some_test

        self.collector.collect_tests(module_mock)

        assert_that(len(self.collector.test_suite)).equals(0)

    def test_should_collect_two_tests_from_module (self):
        @test
        def some_test ():
            pass

        @test
        def some_other_test ():
            pass

        module_mock = mock()
        module_mock.some_test = some_test
        module_mock.some_other_test = some_other_test

        self.collector.collect_tests(module_mock)

        assert_that(len(self.collector.test_suite)).equals(2)
