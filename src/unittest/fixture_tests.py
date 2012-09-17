__author__ = "Alexander Metzner"

import unittest
from pyassert import assert_that

from pyfix.fixture import ConstantFixture

class ConstantFixtureTest (unittest.TestCase):
    def test_ensure_that_provide_returns_set_value (self):
        value = "spam"
        fixture = ConstantFixture(value)
        assert_that(fixture.provide()).is_identical_to(value)
