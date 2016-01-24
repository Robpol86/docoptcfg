"""Test environment variable handling."""

import os

import pytest

from docoptcfg import docoptcfg
from tests import DOCSTRING_FAM, DOCSTRING_MULTI, DOCSTRING_NOT_MULTI, EXPECTED_FAM, EXPECTED_MULTI, EXPECTED_NOT_MULTI


@pytest.mark.parametrize('set_config,set_verbose', [
    (None, None),
    ('', ''),
    ('config.inf', 'true'),
    ('/tmp/config.ini', ' True'),
    (None, 'TRUE '),
    (None, 'false'),
    (None, 'False'),
    (None, 'FALSE'),
    (None, '0'),
    (None, '1'),
    (None, 'None'),
    (None, 'considered_false'),
])
def test(monkeypatch, set_config, set_verbose):
    """Test with env variables.

    :param monkeypatch: pytest fixture.
    :param str set_config: Set FAM_CONFIG to this value if not None.
    :param str set_verbose: Set FAM_VERBOSE to this value if not None.
    """
    monkeypatch.setenv('FAM_HELP', 'True')
    monkeypatch.setenv('FAM_VERSION', 'True')

    expected = EXPECTED_FAM.copy()
    if set_config is not None:
        expected['--config'] = str(set_config)
        monkeypatch.setenv('FAM_CONFIG', set_config)
    if set_verbose is not None:
        if set_verbose.strip().lower() in ('true', '1'):
            expected['--verbose'] = True
        monkeypatch.setenv('FAM_VERBOSE', set_verbose)

    actual = docoptcfg(DOCSTRING_FAM, ['run'], env_prefix='FAM_')
    assert actual == expected


@pytest.mark.parametrize('short', [False, True])
@pytest.mark.parametrize('equals', [False, True])
def test_override(monkeypatch, short, equals):
    """Test overriding env variables with command line.

    :param monkeypatch: pytest fixture.
    :param bool short: Use short arg names.
    :param bool equals: Use ['--key=val'] or ['-kval'] instead of ['--key', 'val'].
    """
    monkeypatch.setenv('FAM_FFMPEG_BIN', '/tmp/ffmpeg')
    monkeypatch.setenv('FAM_VERBOSE', 'False')

    if equals and short:
        argv = ['run', '-f/tmp/arg/ffmpeg', '-v']
    elif equals:
        argv = ['run', '--ffmpeg-bin=/tmp/arg/ffmpeg', '--verbose']
    else:
        argv = ['run', '--ffmpeg-bin', '/tmp/arg/ffmpeg', '--verbose']

    actual = docoptcfg(DOCSTRING_FAM, argv, env_prefix='FAM_')
    expected = EXPECTED_FAM.copy()
    expected['--ffmpeg-bin'] = '/tmp/arg/ffmpeg'
    expected['--verbose'] = True
    assert actual == expected

    actual = docoptcfg(DOCSTRING_FAM, ['run'], env_prefix='FAM_')
    expected = EXPECTED_FAM.copy()
    expected['--ffmpeg-bin'] = '/tmp/ffmpeg'
    expected['--verbose'] = False
    assert actual == expected


@pytest.mark.parametrize('short', [False, True])
def test_docopt_default(monkeypatch, short):
    """Test compatibility with "default" feature in docopt.

    :param monkeypatch: pytest fixture.
    :param bool short: Use short arg names.
    """
    monkeypatch.setenv('FAM_THREADS', '2')

    # Test override.
    actual = docoptcfg(DOCSTRING_FAM, ['run', '-t' if short else '--threads', '1'], env_prefix='FAM_')
    expected = EXPECTED_FAM.copy()
    expected['--threads'] = '1'
    assert actual == expected

    # Test "default".
    actual = docoptcfg(DOCSTRING_FAM, ['run'], env_prefix='FAM_')
    expected = EXPECTED_FAM.copy()
    expected['--threads'] = '2'
    assert actual == expected


@pytest.mark.parametrize('set_flag', ['0', '1', '2', '3', '', 'consider_false', None])
@pytest.mark.parametrize('multi', [False, True])
def test_multi_flag(monkeypatch, multi, set_flag):
    """Test with repeatable flag/boolean option.

    :param monkeypatch: pytest fixture.
    :param bool multi: Test with ... and without ... in docstring.
    :param str set_flag: Set MULTI_FLAG to this value if not None.
    """
    monkeypatch.setattr('sys.argv', ['pytest'])
    docstring = DOCSTRING_MULTI if multi else DOCSTRING_NOT_MULTI
    expected = EXPECTED_MULTI.copy() if multi else EXPECTED_NOT_MULTI.copy()

    if set_flag is not None:
        monkeypatch.setenv('MULTI_FLAG', set_flag)
        if not multi and set_flag == '1':
            expected['--flag'] = True
        elif not multi:
            expected['--flag'] = False
        elif set_flag.isdigit():
            expected['--flag'] = int(set_flag)
        else:
            expected['--flag'] = 0

    actual = docoptcfg(docstring, env_prefix='MULTI_')
    assert actual == expected


@pytest.mark.parametrize('set_key1', [None, '', 'c'])
@pytest.mark.parametrize('set_key0', [None, '', 'b'])
@pytest.mark.parametrize('set_key', [None, '', 'a'])
@pytest.mark.parametrize('multi', [False, True])
def test_multi(monkeypatch, multi, set_key, set_key0, set_key1):
    """Test with repeatable non-boolean options.

    :param monkeypatch: pytest fixture.
    :param bool multi: Test with ... and without ... in docstring.
    :param str set_key: Set MULTI_KEY to this value if not None.
    :param str set_key0: Set MULTI_KEY0 to this value if not None.
    :param str set_key1: Set MULTI_KEY1 to this value if not None.
    """
    monkeypatch.setattr('sys.argv', ['pytest', '--flag'])
    docstring = DOCSTRING_MULTI if multi else DOCSTRING_NOT_MULTI
    expected = EXPECTED_MULTI.copy() if multi else EXPECTED_NOT_MULTI.copy()
    expected['--flag'] = 1 if multi else True

    # Set variables.
    if set_key is not None:
        monkeypatch.setenv('MULTI_KEY', set_key)
    if set_key0 is not None:
        monkeypatch.setenv('MULTI_KEY0', set_key0)
    if set_key1 is not None:
        monkeypatch.setenv('MULTI_KEY1', set_key1)

    # Test not multi.
    if not multi:
        if set_key is not None:
            expected['--key'] = str(set_key)  # Others are ignored.
        actual = docoptcfg(docstring, env_prefix='MULTI_')
        assert actual == expected
        return

    set_keys = (set_key is not None, set_key0 is not None, set_key1 is not None)
    if set_keys == (True, True, True):
        expected['--key'] = [set_key, set_key0, set_key1]
    elif set_keys == (True, True, False):
        expected['--key'] = [set_key, set_key0]
    elif set_keys == (True, False, False):
        expected['--key'] = [set_key]

    elif set_keys == (False, False, False):
        expected['--key'] = []
    elif set_keys == (False, False, True):
        expected['--key'] = []
    elif set_keys == (False, True, True):
        expected['--key'] = [set_key0, set_key1]

    elif set_keys == (False, True, False):
        expected['--key'] = [set_key0]
    elif set_keys == (True, False, True):
        expected['--key'] = [set_key]

    else:
        raise NotImplementedError

    actual = docoptcfg(docstring, env_prefix='MULTI_')
    assert actual == expected


def test_multi_a_lot(monkeypatch):
    """Test setting >99 env variables. For branch coverage.

    :param monkeypatch: pytest fixture.
    """
    expected = EXPECTED_MULTI.copy()
    monkeypatch.setenv('MULTI_FLAG', '1')  # Ignore.
    for i in range(100):
        monkeypatch.setenv('MULTI_KEY{0}'.format(i), str(i))
        if i < 99:
            expected['--key'].append(str(i))
    actual = docoptcfg(DOCSTRING_MULTI, [], ignore=('-h', '-V', '--flag'), env_prefix='MULTI_')
    assert actual == expected
    assert 'MULTI_KEY99' in os.environ
    assert '99' not in actual['--key']
