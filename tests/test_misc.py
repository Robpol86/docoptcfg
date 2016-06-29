"""Miscellaneous tests for test coverage."""

from docoptcfg import docoptcfg
from tests import DOCSTRING_MULTI, EXPECTED_MULTI


def test_no_settable():
    """Test with all options overridden by command line."""
    actual = docoptcfg(DOCSTRING_MULTI, ['1', '--config=config.ini', '--flag', '--key=val'], env_prefix='MULTI_')
    expected = EXPECTED_MULTI.copy()
    expected['--config'] = 'config.ini'
    expected['--flag'] = 1
    expected['--key'] = ['val']
    assert actual == expected
