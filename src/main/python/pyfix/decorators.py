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

TEST_ATTRIBUTE = "pyfix_test"
GIVEN_ATTRIBUTE = "pyfix_given"
BEFORE_ATTRIBUTE = "pyfix_before"
AFTER_ATTRIBUTE = "pyfix_after"

_DUPLICATE_FIXTURE_NAME_PATTERN = "Unable to define fixture with name '{0}' and value '{1}' because it is already given with value '{2}'"

def test(function):
    """
    Marks a function as a test:

    @test
    def ensure_that_something_is_valid (...):
        ...
    """
    setattr(function, TEST_ATTRIBUTE, True)
    return function


def given(**fixture_demands):
    """
    Defines expectations that have to be fulfilled before a test method is executed. Givens are values that are
    computed by the framework and passed to the test function using named parameters.

    Consider this example:

      @test
      @given(spam=Spam)
      def some_test(spam): pass

    In this example the framework would create an instance of class Spam and pass it to the test function via the named
    'spam' parameter.

    You can use multiple given decorators or use more than one named argument for any given decorator.
    """
    if not len(fixture_demands):
        raise ValueError("No fixtures given.")

    def mark_demands(function):
        givens = {}
        if hasattr(function, GIVEN_ATTRIBUTE):
            givens = getattr(function, GIVEN_ATTRIBUTE)

        for name in fixture_demands:
            if name in givens:
                raise ValueError(
                    _DUPLICATE_FIXTURE_NAME_PATTERN.format(
                        name, fixture_demands[name], givens[name]))
            givens[name] = fixture_demands[name]

        setattr(function, GIVEN_ATTRIBUTE, givens)

        return function

    return mark_demands


def _add_interceptors(function, attribute_name, interceptors):
    for interceptor in interceptors:
        if not callable(interceptor):
            raise ValueError("Interceptor '{0}' is not callable".format(interceptor))

    registered_interceptors = []

    if hasattr(function, attribute_name):
        registered_interceptors = getattr(function, attribute_name)

    registered_interceptors = list(interceptors) + registered_interceptors
    setattr(function, attribute_name, registered_interceptors)

    return function


def before(*interceptors):
    """
    Registers the given interceptors to be executed before the decorated test method:

      def interceptor (): pass

      @test
      @before(interceptor)
      def some_test (): pass

    You can use multiple before decorators and/ or pass in multiple values.
    """

    def add_interceptors(function):
        return _add_interceptors(function, BEFORE_ATTRIBUTE, interceptors)

    return add_interceptors


def after(*interceptors):
    """
    Registers the given interceptors to be executed after the decorated test method:

      def interceptor (): pass

      @test
      @after(interceptor)
      def some_test (): pass

    You can use multiple after decorators and/ or pass in multiple values.
    """

    def add_interceptors(function):
        return _add_interceptors(function, AFTER_ATTRIBUTE, interceptors)

    return add_interceptors
