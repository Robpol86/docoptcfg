"""docopt wrapper adding config file and environment variable support.

https://github.com/Robpol86/docoptcfg
https://pypi.python.org/pypi/docoptcfg
"""

import os
import sys

from docopt import docopt, parse_defaults

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
    docopt_dict = docopt(doc, argv, *args, **kwargs)
    if env_prefix is None and config_option is None:
        return docopt_dict  # Nothing to do.
    if argv is None:
        argv = sys.argv[1:]
    if ignore is None:
        ignore = ('--help', '--version')

    # Determine which options are settable by docoptcfg and which ones are flags/booleans.
    settable = list()
    booleans = list()
    for option in parse_defaults(doc):
        if option.long in argv or option.short in argv:
            continue  # Overridden by command line arguments.
        if option.long in ignore or option.short in ignore:
            continue
        if option.argcount == 0:
            booleans.append(option.long)
        settable.append(option.long)

    # Handle environment variables defaults.
    defaults = dict()
    if env_prefix is not None:
        for key in (k for k in docopt_dict if k in settable):
            env_name = '{0}{1}'.format(env_prefix, key[2:].replace('-', '_').upper())
            if env_name not in os.environ:
                continue
            if key in booleans:
                defaults[key] = os.environ[env_name].strip().lower() in ('true', '1')
            else:
                defaults[key] = os.environ[env_name]

    # Merge dicts.
    final_dict = docopt_dict.copy()
    final_dict.update(defaults)
    return final_dict
