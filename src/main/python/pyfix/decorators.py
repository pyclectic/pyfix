__author__ = "Alexander Metzner"

TEST_ATTRIBUTE = "pyfix_test"
GIVEN_ATTRIBUTE = "pyfix_given"

_DUPLICATE_FIXTURE_NAME_PATTERN = "Unable to define fixture with name '{0}' and value '{1}' because it is already given with value '{2}'"

def test (function):
    """
    Marks a function as a test:

    @test
    def ensure_that_something_is_valid (...):
        ...
    """
    setattr(function, TEST_ATTRIBUTE, True)
    return function


def given (**fixtureDemands):
    if len(fixtureDemands) == 0:
        raise ValueError("No fixtures given.")

    def mark_demands (function):
        givens = {}
        if hasattr(function, GIVEN_ATTRIBUTE):
            givens = getattr(function, GIVEN_ATTRIBUTE)

        for name in fixtureDemands:
            if name in givens:
                raise ValueError(
                    _DUPLICATE_FIXTURE_NAME_PATTERN.format(
                        name, fixtureDemands[name], givens[name]))
            givens[name] = fixtureDemands[name]

        setattr(function, GIVEN_ATTRIBUTE, givens)

        return function

    return mark_demands