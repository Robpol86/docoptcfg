"""Miscellaneous tests for test coverage."""

from docoptcfg import docoptcfg
from tests import DOCSTRING_MULTI


def test_no_settable():
    """Test with all options overridden by command line."""
    actual = docoptcfg(DOCSTRING_MULTI, ['--config=config.ini', '--flag', '--key=val'], env_prefix='MULTI_')
    expected = {'--config': 'config.ini', '--flag': 1, '--key': ['val']}
    assert actual == expected
