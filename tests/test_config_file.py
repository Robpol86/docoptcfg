"""Test config file handling."""

import os
from textwrap import dedent

import pytest

from docoptcfg import docoptcfg, DocoptcfgError, DocoptcfgFileError
from tests import DOCSTRING_FAM, DOCSTRING_MULTI, DOCSTRING_NOT_MULTI, EXPECTED_FAM, EXPECTED_MULTI, EXPECTED_NOT_MULTI


def test_none():
    """Test when user doesn't specify a config file."""
    expected = EXPECTED_FAM.copy()
    actual = docoptcfg(DOCSTRING_FAM, ['run'], config_option='--config')
    assert actual == expected


@pytest.mark.parametrize('argv_short', [False, True])
@pytest.mark.parametrize('option_short', [False, True])
def test(tmpdir, argv_short, option_short):
    """Test with sample config file.

    :param tmpdir: pytest fixture.
    :param bool argv_short: Use short name for argv option.
    :param bool option_short: Use short name for config_option value.
    """
    config_file = tmpdir.join('config.ini')
    config_file.write(dedent("""\
    [FlashAirMusic]
    config = /tmp/ignore.me
    ffmpeg-bin = ffmpeg
    help = True
    mac-addr =
    quiet = true
    threads = 9
    version = True
    """))

    argv = ['run', '-c' if argv_short else '--config', str(config_file)]

    actual = docoptcfg(DOCSTRING_FAM, argv, config_option='-c' if option_short else '--config')
    expected = EXPECTED_FAM.copy()
    expected['--config'] = str(config_file)
    expected['--ffmpeg-bin'] = 'ffmpeg'
    expected['--mac-addr'] = ''
    expected['--quiet'] = True
    expected['--threads'] = '9'
    assert actual == expected


def test_errors(tmpdir):
    """Test error handling.

    :param tmpdir: pytest fixture.
    """
    config_file = tmpdir.join('config.ini')
    argv = ['run', '-c', str(config_file)]

    # Test bad config_option value.
    with pytest.raises(DocoptcfgError):
        docoptcfg(DOCSTRING_FAM, argv, config_option='--config-file')

    # Test missing file.
    with pytest.raises(DocoptcfgFileError) as exc:
        docoptcfg(DOCSTRING_FAM, argv, config_option='-c')
    assert exc.value.message == 'Unable to read config file.'
    assert exc.value.FILE_PATH == str(config_file)
    assert 'No such file or directory' in exc.value.original_error

    # Test permission error.
    if os.name != 'nt':
        config_file.ensure().chmod(0o0244)
        with pytest.raises(DocoptcfgFileError) as exc:
            docoptcfg(DOCSTRING_FAM, argv, config_option='-c')
        assert exc.value.message == 'Unable to read config file.'
        assert exc.value.FILE_PATH == str(config_file)
        assert 'Permission denied' in exc.value.original_error

    # Test empty file.
    config_file.ensure().chmod(0o0644)
    with pytest.raises(DocoptcfgFileError) as exc:
        docoptcfg(DOCSTRING_FAM, argv, config_option='-c')
    assert exc.value.message == 'Section [FlashAirMusic] not in config file.'
    assert exc.value.FILE_PATH == str(config_file)
    assert exc.value.original_error is None

    # Test corrupt file.
    config_file.write('\x00\x00\x00\x00')
    with pytest.raises(DocoptcfgFileError) as exc:
        docoptcfg(DOCSTRING_FAM, argv, config_option='-c')
    assert exc.value.message == 'Unable to parse config file.'
    assert exc.value.FILE_PATH == str(config_file)
    assert 'File contains no section headers.' in exc.value.original_error

    # Test bad boolean.
    config_file.write('[FlashAirMusic]\nverbose = "test"')
    with pytest.raises(DocoptcfgFileError) as exc:
        docoptcfg(DOCSTRING_FAM, argv, config_option='-c')
    assert exc.value.message == 'Boolean option "verbose" invalid.'
    assert exc.value.FILE_PATH == str(config_file)
    assert 'Not a boolean' in exc.value.original_error


@pytest.mark.parametrize('short', [False, True])
@pytest.mark.parametrize('equals', [False, True])
def test_override(tmpdir, short, equals):
    """Test overriding config values with command line.

    :param tmpdir: pytest fixture.
    :param bool short: Use short arg names.
    :param bool equals: Use ['--key=val'] or ['-kval'] instead of ['--key', 'val'].
    """
    config_file = tmpdir.join('config.ini')
    config_file.write(dedent("""\
    [FlashAirMusic]
    ffmpeg-bin=/tmp/ffmpeg
    verbose=false
    """))

    if equals and short:
        argv = ['run', '-c', str(config_file), '-f/tmp/arg/ffmpeg', '-v']
    elif equals:
        argv = ['run', '-c', str(config_file), '--ffmpeg-bin=/tmp/arg/ffmpeg', '--verbose']
    else:
        argv = ['run', '-c', str(config_file), '--ffmpeg-bin', '/tmp/arg/ffmpeg', '--verbose']

    actual = docoptcfg(DOCSTRING_FAM, argv, config_option='--config')
    expected = EXPECTED_FAM.copy()
    expected['--config'] = str(config_file)
    expected['--ffmpeg-bin'] = '/tmp/arg/ffmpeg'
    expected['--verbose'] = True
    assert actual == expected

    actual = docoptcfg(DOCSTRING_FAM, ['run', '-c', str(config_file)], config_option='--config')
    expected = EXPECTED_FAM.copy()
    expected['--config'] = str(config_file)
    expected['--ffmpeg-bin'] = '/tmp/ffmpeg'
    expected['--verbose'] = False
    assert actual == expected


@pytest.mark.parametrize('short', [False, True])
def test_docopt_default(tmpdir, short):
    """Test compatibility with "default" feature in docopt.

    :param tmpdir: pytest fixture.
    :param bool short: Use short arg names.
    """
    config_file = tmpdir.join('config.ini')
    config_file.write(dedent("""\
    [FlashAirMusic]
    threads=2
    """))

    # Test override.
    argv = ['run', '-c', str(config_file), '-t' if short else '--threads', '1']
    actual = docoptcfg(DOCSTRING_FAM, argv, config_option='--config')
    expected = EXPECTED_FAM.copy()
    expected['--config'] = str(config_file)
    expected['--threads'] = '1'
    assert actual == expected

    # Test "default".
    actual = docoptcfg(DOCSTRING_FAM, ['run', '-c', str(config_file)], config_option='--config')
    expected = EXPECTED_FAM.copy()
    expected['--config'] = str(config_file)
    expected['--threads'] = '2'
    assert actual == expected


@pytest.mark.parametrize('set_flag', ['0', '1', '2', '3', '', 'consider_false', None])
@pytest.mark.parametrize('multi', [False, True])
def test_multi_flag(monkeypatch, tmpdir, multi, set_flag):
    """Test with repeatable flag/boolean option.

    :param monkeypatch: pytest fixture.
    :param tmpdir: pytest fixture.
    :param bool multi: Test with ... and without ... in docstring.
    :param str set_flag: Set flag= to this value if not None.
    """
    config_file = tmpdir.join('config.ini')
    config_file.write('[my_script]\n')

    monkeypatch.setattr('sys.argv', ['pytest', '1', '--config', str(config_file)])
    docstring = DOCSTRING_MULTI if multi else DOCSTRING_NOT_MULTI
    expected = EXPECTED_MULTI.copy() if multi else EXPECTED_NOT_MULTI.copy()
    expected['--config'] = str(config_file)

    if set_flag is not None:
        config_file.write('flag={0}'.format(set_flag), mode='a')
        if not multi and set_flag == '1':
            expected['--flag'] = True
        elif not multi:
            expected['--flag'] = False
        elif set_flag.isdigit():
            expected['--flag'] = int(set_flag)

    if multi and set_flag is not None and not set_flag.isdigit():
        with pytest.raises(DocoptcfgFileError) as exc:
            docoptcfg(docstring, config_option='--config')
        assert exc.value.message == 'Repeatable boolean option "flag" invalid.'
        assert exc.value.FILE_PATH == str(config_file)
        assert 'invalid literal for int()' in exc.value.original_error
        return

    if not multi and set_flag not in (None, '0', '1'):
        with pytest.raises(DocoptcfgFileError) as exc:
            docoptcfg(docstring, config_option='--config')
        assert exc.value.message == 'Boolean option "flag" invalid.'
        assert exc.value.FILE_PATH == str(config_file)
        assert 'Not a boolean' in exc.value.original_error
        return

    actual = docoptcfg(docstring, config_option='--config')
    assert actual == expected


@pytest.mark.parametrize('multi', [False, True])
def test_multi(monkeypatch, tmpdir, multi):
    """Test with repeatable non-boolean options.

    :param monkeypatch: pytest fixture.
    :param tmpdir: pytest fixture.
    :param bool multi: Test with ... and without ... in docstring.
    """
    config_file = tmpdir.join('config.ini')
    config_file.write(dedent("""
    [my_script]
    key =
        a
        b
        c
    """))

    monkeypatch.setattr('sys.argv', ['pytest', '1', '--flag', '--config', str(config_file)])
    docstring = DOCSTRING_MULTI if multi else DOCSTRING_NOT_MULTI
    expected = EXPECTED_MULTI.copy() if multi else EXPECTED_NOT_MULTI.copy()
    expected['--config'] = str(config_file)
    expected['--flag'] = 1 if multi else True
    expected['--key'] = ['a', 'b', 'c'] if multi else '\na\nb\nc'

    actual = docoptcfg(docstring, config_option='--config')
    assert actual == expected
