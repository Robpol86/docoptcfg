"""Test environment variable handling."""

import pytest

from docoptcfg import docoptcfg
from tests import DOCSTRING_FAM, EXPECTED_FAM


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
    :param str set_verbose: Set FAM_VERBOSE to this value of not None.
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
def test_override(monkeypatch, short):
    """Test overriding env variables with command line.

    :param monkeypatch: pytest fixture.
    :param bool short: Use short arg names.
    """
    monkeypatch.setenv('FAM_FFMPEG_BIN', '/tmp/ffmpeg')
    monkeypatch.setenv('FAM_VERBOSE', 'False')

    actual = docoptcfg(DOCSTRING_FAM, [
        'run',
        '-f' if short else '--ffmpeg-bin', '/tmp/arg/ffmpeg',
        '-v' if short else '--verbose',
    ], env_prefix='FAM_')
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
