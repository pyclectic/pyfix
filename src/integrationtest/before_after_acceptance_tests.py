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
