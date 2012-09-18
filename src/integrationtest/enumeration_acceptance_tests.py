__author__ = "Alexander Metzner"

from pyfix import test, run_tests, given, enumerate
from pyassert import assert_that

KNOWN_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19]

def is_prime(number):
    return number in KNOWN_PRIMES


@test
@given(number=enumerate(2, 3, 5, 7, 11))
def is_prime_should_return_true_when_prime_is_given(number):
    assert_that(is_prime(number)).is_true()


if __name__ == "__main__":
    run_tests()
