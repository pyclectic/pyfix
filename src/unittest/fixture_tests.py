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
from pyassert import assert_that

from pyfix.fixture import Fixture, ConstantFixture, EnumeratingFixture, enumerate


class FixtureTest(unittest.TestCase):
    def test_should_return_string_description_when_string_is_given (self):
        assert_that(Fixture().describe("spam")).equals("spam")

    def test_should_return_number_description_when_number_is_given (self):
        assert_that(Fixture().describe(1234)).equals("1234")

    def test_should_return_shortened_description_when_value_is_too_long (self):
        assert_that(Fixture().describe("spam and eggs")).equals("spam ..")


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


class EnumerateTest(unittest.TestCase):
    def test_ensure_that_provide_returns_set_value(self):
        actual = enumerate("spam", "eggs").provide()

        assert_that(len(actual)).equals(2)
        assert_that(actual[0]).equals("spam")
        assert_that(actual[1]).equals("eggs")
