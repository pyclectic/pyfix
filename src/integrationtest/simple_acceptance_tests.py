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
