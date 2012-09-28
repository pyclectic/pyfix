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

from pyfix import test, run_tests, given, Fixture
from pyassert import assert_that

class Accumulator(object):
    def __init__(self):
        self.sum = 0

    def add(self, number=1):
        self.sum += number


class InitializedAccumulator(Fixture):
    def provide(self):
        result = Accumulator()
        result.add(2)
        return [result]


@test
@given(accumulator=Accumulator)
def ensure_that_adding_two_yields_two(accumulator):
    accumulator.add(2)
    assert_that(accumulator.sum).equals(2)


@test
@given(accumulator=InitializedAccumulator)
def ensure_that_adding_two_to_two_yields_four(accumulator):
    accumulator.add(2)
    assert_that(accumulator.sum).equals(4)

if __name__ == "__main__":
    run_tests()
