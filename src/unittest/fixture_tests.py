__author__ = "Alexander Metzner"

import unittest
from pyassert import assert_that

from pyfix.fixture import ConstantFixture, EnumeratingFixture, enumerate


class EnumeratingFixtureTest(unittest.TestCase):
    def test_ensure_that_provide_returns_set_value(self):
        actual = EnumeratingFixture(["spam", "eggs"]).provide()

        assert_that(len(actual)).equals(2)
        assert_that(actual[0]).equals("spam")
        assert_that(actual[1]).equals("eggs")


class ConstantFixtureTest(unittest.TestCase):
    def test_ensure_that_provide_returns_set_value(self):
        value = "spam"
        actual = ConstantFixture(value).provide()

        assert_that(len(actual)).equals(1)
        assert_that(actual[0]).is_identical_to(value)

class EnumerateTest (unittest.TestCase):
    def test_ensure_that_provide_returns_set_value(self):
        actual = enumerate("spam", "eggs").provide()

        assert_that(len(actual)).equals(2)
        assert_that(actual[0]).equals("spam")
        assert_that(actual[1]).equals("eggs")
