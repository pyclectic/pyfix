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
