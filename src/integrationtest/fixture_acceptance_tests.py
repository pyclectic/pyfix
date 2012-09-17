__author__ = "Alexander Metzner"

from pyfix import test, run_tests, given, Fixture
from pyassert import assert_that

class Accumulator(object):
    def __init__ (self):
        self.sum = 0

    def add (self, number=1):
        self.sum += number

class InitializedAccumulator (Fixture):
    def provide (self):
        result = Accumulator()
        result.add(2)
        return result

@test
@given(accumulator=Accumulator)
def ensure_that_adding_two_yields_two (accumulator):
    accumulator.add(2)
    assert_that(accumulator.sum).equals(2)

@test
@given(accumulator=InitializedAccumulator)
def ensure_that_adding_two_to_two_yields_four (accumulator):
    accumulator.add(2)
    assert_that(accumulator.sum).equals(4)

if __name__ == "__main__":
    run_tests()
