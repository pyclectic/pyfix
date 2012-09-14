__author__ = "Alexander Metzner"

import unittest
from pyassert import assert_that

from pyfix.utils import *

class HumanizeUnderscoreNameTest(unittest.TestCase):
    def test_should_humanize_name_with_underscores (self):
        assert_that(humanize_underscore_name("ensure_that_name_is_ok")).equals("Ensure that name is ok")

    def test_should_not_change_name_without_underscores (self):
        assert_that(humanize_underscore_name("ensureThatNameIsOk")).equals("ensureThatNameIsOk")


class HumanizeCamelCaseNameTest(unittest.TestCase):
    def test_should_not_change_name_without_camelcase (self):
        assert_that(humanize_camel_case_name("ensure_that_name_is_ok")).equals("ensure_that_name_is_ok")

    def test_should_humanize_name_with_camelcase (self):
        assert_that(humanize_camel_case_name("ensureThatNameIsOk")).equals("Ensure that name is ok")

    def test_should_humanize_name_with_camelcase_and_leading_upper_case_letter (self):
        assert_that(humanize_camel_case_name("EnsureThatNameIsOk")).equals("Ensure that name is ok")
