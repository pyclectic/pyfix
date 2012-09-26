__author__ = "Alexander Metzner"

from pyfix import test, run_tests
from pyassert import assert_that

@test
def ensure_that_two_plus_two_equals_four():
    assert_that(2 + 2).equals(4)


@test
def ensure_that_two_plus_three_equals_five():
    assert_that(2 + 3).equals(5)


if __name__ == "__main__":
    run_tests()
