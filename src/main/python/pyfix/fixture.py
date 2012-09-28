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


class Fixture(object):
    """
    Base class for objects that provide values to be injected to test functions.
    """

    def provide(self):
        "Called by the framework to obtain the list of values to be passed in to a test."
        pass

    def reclaim(self, value):
        "Called by the framework after the test finished (successfully or not) to allow the fixture to do some cleanup."
        pass

    def describe(self, value):
        "Provides a description for the given value. The value has been obtained from the list of obtained values."

        candidate = str(value)

        if len(candidate) > 7:
            candidate = candidate[0:5] + ".."

        return candidate


class ConstantFixture(Fixture):
    """
    Fixture used as a decorator to serve constant values.
    """

    def __init__(self, value):
        self._value = [value]

    def provide(self):
        return self._value


class EnumeratingFixture(Fixture):
    """
    Fixture that enumerates all given values providing more then one value
    """

    def __init__(self, values):
        self._values = values

    def provide(self):
        return self._values


def enumerate(*values):
    "Convenience function that returns a new instance of an EnumeratingFixture"
    return EnumeratingFixture(values)
