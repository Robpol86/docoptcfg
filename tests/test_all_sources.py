"""Test combination of all sources."""

from textwrap import dedent

import pytest

from docoptcfg import docoptcfg
from tests import DOCSTRING_FAM, EXPECTED_FAM


def test_config_file_in_env(monkeypatch, tmpdir):
    """Test specifying a config file using only env variables.

    :param monkeypatch: pytest fixture.
    :param tmpdir: pytest fixture.
    """
    config_file = tmpdir.join('config.ini')
    config_file.write(dedent("""\
    [FlashAirMusic]
    mac-addr = AA:BB:CC:DD:EE:FF
    """))

    monkeypatch.setenv('FAM_CONFIG', str(config_file))
    actual = docoptcfg(DOCSTRING_FAM, ['run'], config_option='-c', env_prefix='FAM_')
    expected = EXPECTED_FAM.copy()
    expected['--config'] = str(config_file)
    expected['--mac-addr'] = 'AA:BB:CC:DD:EE:FF'
    assert actual == expected


@pytest.mark.parametrize('set_arg', [True, False])
@pytest.mark.parametrize('set_env', [True, False])
@pytest.mark.parametrize('set_file', [True, False])
def test_override(monkeypatch, tmpdir, set_arg, set_env, set_file):
    """Test source overrides.

    :param monkeypatch: pytest fixture.
    :param tmpdir: pytest fixture.
    :param bool set_arg: Set value in command line arguments.
    :param bool set_env: Set value in environment variables.
    :param bool set_file: Set value in config file.
    """
    config_file = tmpdir.join('config.ini')
    config_file.write(dedent("""\
    [FlashAirMusic]
    quiet = true
    {0}
    """).format('ffmpeg-bin = ffmpeg_file' if set_file else ''))

    monkeypatch.setenv('FAM_CONFIG', str(config_file))
    monkeypatch.setenv('FAM_VERBOSE', 'true')
    if set_env:
        monkeypatch.setenv('FAM_FFMPEG_BIN', 'ffmpeg_env')

    argv = ['run', '-m', '00:11:22:33:44:55'] + (['--ffmpeg-bin', 'ffmpeg_arg'] if set_arg else [])

    actual = docoptcfg(DOCSTRING_FAM, argv, config_option='-c', env_prefix='FAM_')
    expected = EXPECTED_FAM.copy()
    expected['--config'] = str(config_file)
    expected['--mac-addr'] = '00:11:22:33:44:55'
    expected['--quiet'] = True
    expected['--verbose'] = True

    if set_arg:
        expected['--ffmpeg-bin'] = 'ffmpeg_arg'
    elif set_env:
        expected['--ffmpeg-bin'] = 'ffmpeg_env'
    elif set_file:
        expected['--ffmpeg-bin'] = 'ffmpeg_file'

    assert actual == expected


@pytest.mark.parametrize('data_type', ['str', 'int', 'float'])
@pytest.mark.parametrize('source', ['arg', 'env', 'file'])
def test_data_types(monkeypatch, tmpdir, source, data_type):
    """Ensure all sources produce the exact same non-boolean data types and values.

    :param monkeypatch: pytest fixture.
    :param tmpdir: pytest fixture.
    :param source: Config source to test.
    :param data_type: Data type to test.
    """
    argv = ['run']
    expected = EXPECTED_FAM.copy()

    if source == 'file':
        config_file = tmpdir.join('config.ini')
        if data_type == 'str':
            config_file.write('[FlashAirMusic]\nmac-addr = one')
        elif data_type == 'int':
            config_file.write('[FlashAirMusic]\nmac-addr = 1')
        else:
            config_file.write('[FlashAirMusic]\nmac-addr = 2.3')
        monkeypatch.setenv('FAM_CONFIG', str(config_file))
        expected['--config'] = str(config_file)

    elif source == 'env':
        if data_type == 'str':
            monkeypatch.setenv('FAM_MAC_ADDR', 'one')
        elif data_type == 'int':
            monkeypatch.setenv('FAM_MAC_ADDR', '1')
        else:
            monkeypatch.setenv('FAM_MAC_ADDR', '2.3')

    else:
        if data_type == 'str':
            argv.extend(['--mac-addr', 'one'])
        elif data_type == 'int':
            argv.extend(['--mac-addr', '1'])
        else:
            argv.extend(['--mac-addr', '2.3'])

    # Set expected.
    if data_type == 'str':
        expected['--mac-addr'] = 'one'
    elif data_type == 'int':
        expected['--mac-addr'] = '1'
    else:
        expected['--mac-addr'] = '2.3'

    actual = docoptcfg(DOCSTRING_FAM, argv, config_option='-c', env_prefix='FAM_')
    assert actual == expected
