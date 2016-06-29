"""Test without environment variables or config file handling."""

from docoptcfg import docoptcfg
from tests import DOCSTRING_FAM, DOCSTRING_MULTI, EXPECTED_FAM, EXPECTED_MULTI


def test_fam(monkeypatch, tmpdir):
    """Make sure config file and environment variables aren't being handled.

    :param monkeypatch: pytest fixture.
    :param tmpdir: pytest fixture.
    """
    monkeypatch.setenv('FFMPEG_BIN', tmpdir.ensure('ffmpeg'))
    tmpdir.join('config.ini').write('[FlashAirMusic]\nmac-addr = 00:11:22:33:44:55')

    actual = docoptcfg(DOCSTRING_FAM, ['run', '--config', str(tmpdir.join('config.ini'))])
    expected = EXPECTED_FAM.copy()
    expected['--config'] = str(tmpdir.join('config.ini'))

    assert actual == expected


def test_multi(monkeypatch, tmpdir):
    """Same with multi options.

    :param monkeypatch: pytest fixture.
    :param tmpdir: pytest fixture.
    """
    monkeypatch.setenv('FFMPEG_BIN', tmpdir.ensure('ffmpeg'))
    tmpdir.join('config.ini').write('[my_script]\nkey = \n    val1,\n    val2')

    actual = docoptcfg(DOCSTRING_MULTI, ['1', '--config', str(tmpdir.join('config.ini'))])
    expected = EXPECTED_MULTI.copy()
    expected['--config'] = str(tmpdir.join('config.ini'))

    assert actual == expected
