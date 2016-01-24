"""Importable objects shared by test modules."""


DOCSTRING_FAM = """\
Sync FLAC music to your car's head unit using a FlashAir WiFi SD card.

Command line options overridden by config file values.

Usage:
    FlashAirMusic [options] run
    FlashAirMusic -h | --help
    FlashAirMusic -V | --version

Options:
    -c FILE --config=FILE       Path YAML config file.
    -f FILE --ffmpeg-bin=FILE   File path to ffmpeg binary.
    -h --help                   Show this screen.
    -l FILE --log=FILE          Log to file. Will be rotated daily.
    -m ADDR --mac-addr=ADDR     FlashAir MAC Address (DHCP sniffing).
    -q --quiet                  Don't print anything to stdout/stderr.
    -s DIR --music-source=DIR   Source directory containing FLAC/MP3s.
    -t NUM --threads=NUM        File conversion worker count [default: 0].
                                0 is one worker per CPU.
    -v --verbose                Debug logging.
    -V --version                Show version and exit.
    -w DIR --working-dir=DIR    Working directory for converted music, etc.
"""
EXPECTED_FAM = {
    '--config': None,
    '--ffmpeg-bin': None,
    '--help': False,
    '--log': None,
    '--mac-addr': None,
    '--music-source': None,
    '--quiet': False,
    '--threads': '0',
    '--verbose': False,
    '--version': False,
    '--working-dir': None,
    'run': True,
}
