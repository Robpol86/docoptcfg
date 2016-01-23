"""docopt wrapper adding config file and environment variable support.

https://github.com/Robpol86/docoptcfg
https://pypi.python.org/pypi/docoptcfg
"""

from docopt import docopt

__all__ = ('docoptcfg',)
__author__ = '@Robpol86'
__license__ = 'MIT'
__version__ = '0.0.1'


def docoptcfg(doc, argv=None, env_prefix=None, config_option=None, ignore=None, *args, **kwargs):
    """Pass most args/kwargs to docopt. Handle `env_prefix` and `config_option`.

    :param str doc: Docstring passed to docopt.
    :param iter argv: sys.argv[1:] passed to docopt.
    :param str env_prefix: Enable environment variable support, prefix of said variables.
    :param str config_option: Enable config file support, docopt option defining path to config file.
    :param iter ignore: Options to ignore. Default is --help and --version.
    :param iter args: Additional positional arguments passed to docopt.
    :param dict kwargs: Additional keyword arguments passed to docopt.

    :return: Dictionary constructed by docopt and updated by docoptcfg.
    :rtype: dict
    """
    assert env_prefix is None
    assert config_option is None
    assert ignore is None
    return docopt(doc, argv, *args, **kwargs)
