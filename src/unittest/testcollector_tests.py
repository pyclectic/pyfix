__author__ = "Alexander Metzner"

import unittest
from mockito import mock
from pyassert import assert_that

from pyfix.testcollector import test, TEST_ATTRIBUTE, TestCollector, TestDefinition

class TestDecoratorTest(unittest.TestCase):
    def test_should_mark_function_as_test (self):
        @test
        def some_test ():
            pass

        assert_that(hasattr(some_test, TEST_ATTRIBUTE)).is_true()

    def test_ensure_that_decorated_function_can_be_called (self):
        @test
        def some_test ():
            some_test.called = True

        some_test.called = False
        some_test()
        assert_that(some_test.called).is_true()


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
