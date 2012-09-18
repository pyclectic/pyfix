__author__ = "Alexander Metzner"


class Fixture(object):
    """
    Base class for objects that provide values to be injected to test functions.
    """

    def provide(self):
        "Called by the framework to obtain the list of values to be passed in to a test."
        pass

    def reclaim(self, value):
        "Called by the framework after the test finished (successfully or not) to allow the fixture to do some cleanup."
        pass

    def describe(self, value):
        "Provides a description for the given value. The value has been obtained from the list of obtained values."

        candidate = str(value)

        if len(candidate) > 7:
            candidate = candidate[0:5] + ".."

        return candidate


class ConstantFixture(Fixture):
    """
    Fixture used as a decorator to serve constant values.
    """

    def __init__(self, value):
        self._value = [value]

    def provide(self):
        return self._value


class EnumeratingFixture(Fixture):
    """
    Fixture that enumerates all given values providing more then one value
    """

    def __init__(self, values):
        self._values = values

    def provide(self):
        return self._values


def enumerate(*values):
    "Convenience function that returns a new instance of an EnumeratingFixture"
    return EnumeratingFixture(values)
