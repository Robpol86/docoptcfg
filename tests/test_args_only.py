"""Test without environment variables or config file handling."""

from docoptcfg import docoptcfg
from tests import DOCSTRING_FAM, EXPECTED_FAM


def test(monkeypatch, tmpdir):
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
