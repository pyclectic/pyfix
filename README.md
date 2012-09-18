
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
pyfix version 0.1.3.

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

```python
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

### Parameterized Tests: Providing more than one Value

As you might have noticed in the last example, the `provide` method from the `Fixture` returned a list and not
just a single value. Every fixture can return more than one value. *pyfix* will use all values provided by all
fixtures and calculate all valid permutations of parameter values and then invoke a single test method for each
permutation. Using this feature it is easy to write parameterized tests.

The simplest variant of a parameterized test is a test accepting one parameter that we provide a set of values for.
*pyfix* provides the `enumerate` utility function to let you write such a test in an easy way:

```python
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
```

Please notice that this example is intended to demonstrate the test and not the implementation of `is_prime` which
indeed is brain dead.

If you run this module you should see an output like the following:

```
pyfix version 0.1.3.

Running 1 tests.
--------------------------------------------------------------------------------
Is prime should return true when prime is given:
	number=2: passed [0 ms]
	number=3: passed [0 ms]
	number=5: passed [0 ms]
	number=7: passed [0 ms]
	number=11: passed [0 ms]
--------------------------------------------------------------------------------
TEST RESULTS SUMMARY
	  5 tests executed in 0 ms
	  0 tests failed
ALL TESTS PASSED
```

## Release Notes
### Version 0.1.3 released 2012-09-18
* Implemented enumerating fixtures like `enumerate`

### Version 0.1.2 released 2012-09-17
* Renamed `main` to `run_tests`

### Version 0.1.1 released 2012-09-14
* Inital release

## License
pyfix is published under the terms of the [Apache License, Version 2](http://www.apache.org/licenses/LICENSE-2.0.html).

## Additional Links
* [pyfix on Cheesshop](http://pypi.python.org/pypi/pyfix)
* [pyassert](https://github.com/pyclectic/pyassert) - used for all unit tests in *pyfix* as well as in all examples
* [pybuilder](https://github.com/pybuilder/pybuilder) - used to "build" *pyfix*
