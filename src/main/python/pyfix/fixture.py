__author__ = "Alexander Metzner"


class Fixture(object):
    """
    Base class for objects that provide values to be injected to test functions.
    """

    def provide(self):
        "Called by the framework to obtain the value to be passed in to a test"
        pass

    def reclaim(self, value):
        "Called by the framework after the test finished (successfully or not) to allow the fixture to do some cleanup"
        pass


class ConstantFixture(Fixture):
    """
    Fixture used as a decorator to serve constant values.
    """

    def __init__(self, value):
        self._value = value

    def provide(self):
        return self._value
