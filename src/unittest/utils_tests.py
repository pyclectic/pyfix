__author__ = "Alexander Metzner"

import unittest
from pyassert import assert_that

from pyfix.utils import *

class HumanizeUnderscoreNameTest(unittest.TestCase):
    def test_should_humanize_name_with_underscores(self):
        assert_that(humanize_underscore_name("ensure_that_name_is_ok")).equals("Ensure that name is ok")

    def test_should_not_change_name_without_underscores(self):
        assert_that(humanize_underscore_name("ensureThatNameIsOk")).equals("ensureThatNameIsOk")


class HumanizeCamelCaseNameTest(unittest.TestCase):
    def test_should_not_change_name_without_camelcase(self):
        assert_that(humanize_camel_case_name("ensure_that_name_is_ok")).equals("ensure_that_name_is_ok")

    def test_should_humanize_name_with_camelcase(self):
        assert_that(humanize_camel_case_name("ensureThatNameIsOk")).equals("Ensure that name is ok")

    def test_should_humanize_name_with_camelcase_and_leading_upper_case_letter(self):
        assert_that(humanize_camel_case_name("EnsureThatNameIsOk")).equals("Ensure that name is ok")


class IsCallableTest(unittest.TestCase):
    def test_should_consider_function_as_callable(self):
        def fun(): pass

        assert_that(is_callable(fun)).is_true()

    def test_should_consider_object_with_call_method_as_callable(self):
        class Spam:
            def __call__(self): pass

        assert_that(is_callable(Spam())).is_true()

    def test_should_consider_bound_method_as_callable(self):
        class Spam:
            def spam(self): pass

        spam = Spam()

        assert_that(is_callable(spam.spam)).is_true()

    def test_should_not_consider_object_without_call_method_as_callable(self):
        class Spam: pass

        assert_that(is_callable(Spam())).is_false()
