
#pyfix [![Build Status](https://secure.travis-ci.org/halimath/pyfix.png?branch=master)](http://travis-ci.org/halimath/pyfix)

pyfix is a test framework for Python.

##Introduction

pyfix is a framework used to write automated software tests. It is similar to tools like
[unittest](http://docs.python.org/library/unittest.html) in purpose but unlike most of the unit testing frameworks being
around today it is not based on the [xUnit](http://en.wikipedia.org/wiki/XUnit) design.

pyfix can be used for different types of tests (including unit tests, integration tests, system tests, functional tests
and even acceptance tests) although the primary targets are more technical tests (such as unit or integration tests).

## How to install it?

pyfix is available via the [Cheeseshop](http://pypi.python.org/pypi/pyfix/) so you can use `easy_install` or `pip`:

```bash
$ pip install pyfix
```

## How to use it?

pyfix focusses on writing test functions. Each test a function that lives in module. Here is some trival example (the
use of [pyassert](https://github.com/halimath/pyassert) is not mandatory although it follows the same idea of having
easy to read tests).

```python
from pyfix import test, run_tests
from pyassert import assert_that

@test
def ensure_that_two_plus_two_equals_four ():
    assert_that(2 + 2).equals(4)

@test
def ensure_that_two_plus_three_equals_five ():
    assert_that(2 + 3).equals(5)

if __name__ == "__main__":
    run_tests()
```

If you execute this file you should see the following output:

```
pyfix version 0.1.1.

Running 2 tests.
--------------------------------------------------------------------------------
Ensure that two plus three equals five: passed [0 ms]
Ensure that two plus two equals four: passed [0 ms]
--------------------------------------------------------------------------------
TEST RESULTS SUMMARY
	  2 tests executed
	  0 tests failed
ALL TESTS PASSED
```

### Fixtures: Injecting values

One of the main strengths of pyfix is the ability to inject parameters to tests. See this example:

```python
from pyfix import test, run_tests, given
from pyassert import assert_that

class Accumulator(object):
    def __init__ (self):
        self.sum = 0

    def add (self, number=1):
        self.sum += number


@test
@given(accumulator=Accumulator)
def ensure_that_adding_two_yields_two (accumulator):
    accumulator.add(2)
    assert_that(accumulator.sum).equals(2)


if __name__ == "__main__":
    run_tests()
```

pyfix will instantiate an `Accumulator` for you and *inject* it using the accumulator parameter. Note that there is
nothing special about the `Accumulator`; it's a plain Python class.

If you want to do some complex initialization and/ or clean up stuff, pyfix provides the `Fixture` interface which
defines hooks for these lifecycle phases.

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
        return [result]


@test
@given(accumulator=InitializedAccumulator)
def ensure_that_adding_two_to_two_yields_four (accumulator):
    accumulator.add(2)
    assert_that(accumulator.sum).equals(4)


if __name__ == "__main__":
    run_tests()
```

## Release Notes
### Version 0.1.2 released 2012-09-17
* Renamed `main` to `run_tests`

### Version 0.1.1 released 2012-09-14
* Inital release

## License
pyfix is published under the terms of the [Apache License, Version 2](http://www.apache.org/licenses/LICENSE-2.0.html).
