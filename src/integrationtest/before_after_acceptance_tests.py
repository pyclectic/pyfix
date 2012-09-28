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

from pyassert import assert_that
from pyfix import test, before, after, run_tests

_BEFORE_EXECUTED = False
_AFTER_EXECUTED = False

def before_interceptor():
    global _BEFORE_EXECUTED
    _BEFORE_EXECUTED = True


def after_interceptor():
    global _AFTER_EXECUTED
    _AFTER_EXECUTED = True


@test
@before(before_interceptor)
def ensure_that_before_interceptor_is_executed():
    assert_that(_BEFORE_EXECUTED).is_true()


@test
@after(after_interceptor)
def ensure_that_after_interceptor_is_executed():
    pass

if __name__ == "__main__":
    run_tests()
    assert_that(_AFTER_EXECUTED).is_true()
