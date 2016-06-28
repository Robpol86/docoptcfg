"""Test with repeatable options."""

from docoptcfg import docoptcfg
from tests import DOCSTRING_MULTI2, EXPECTED_MULTI2


def test():
    """Test with no config file or env variables."""
    actual = docoptcfg(DOCSTRING_MULTI2, ['build', 'destination', 'source1', 'source2'])
    expected = EXPECTED_MULTI2.copy()

    assert actual == expected
