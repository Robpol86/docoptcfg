"""docopt wrapper adding config file and environment variable support.

https://github.com/Robpol86/docoptcfg
https://pypi.python.org/pypi/docoptcfg
"""

import os
import sys

try:
    from ConfigParser import ConfigParser, Error
except ImportError:
    from configparser import ConfigParser, Error

import docopt

__all__ = ('docoptcfg',)
__author__ = '@Robpol86'
__license__ = 'MIT'
__version__ = '1.0.2'


class DocoptcfgError(Exception):
    """Error in docoptcfg usage by developer."""


class DocoptcfgFileError(Exception):
    """Error while reading or parsing config file."""

    FILE_PATH = ''

    def __init__(self, message, original_error=None):
        """Constructor."""
        self.message = message
        self.original_error = original_error
        super(DocoptcfgFileError, self).__init__(message, self.FILE_PATH, original_error)


def settable_options(doc, argv, ignore, options_first):
    """Determine which options we can set, which ones are boolean, and which ones are repeatable.

    All set items are option long names.

    :param str doc: Docstring from docoptcfg().
    :param iter argv: CLI arguments from docoptcfg().
    :param iter ignore: Options to ignore from docoptcfg().
    :param bool options_first: docopt argument from docoptcfg().

    :return: Settable options, boolean options, repeatable options, and short to long option name mapping.
    :rtype: tuple
    """
    settable, booleans, repeatable, short_map = set(), set(), set(), dict()

    # Determine which options are settable by docoptcfg and which ones are flags/booleans.
    options = docopt.parse_defaults(doc)
    short_map.update((o.short, o.long) for o in options)
    parsed_argv = docopt.parse_argv(docopt.TokenStream(argv, docopt.DocoptExit), list(options), options_first)
    overridden = [o.long for o in parsed_argv if hasattr(o, 'long')]
    for option in options:
        if option.long in overridden or (option.long in ignore or option.short in ignore):
            continue
        if option.argcount == 0:
            booleans.add(option.long)
        settable.add(option.long)

    # Determine which options are repeatable.
    if settable and '...' in doc:
        pattern = docopt.parse_pattern(docopt.formal_usage(docopt.DocoptExit.usage), options)
        for option in pattern.fix().flat():
            if not hasattr(option, 'long'):
                continue  # Positional argument or sub-command.
            if option.long not in settable:
                continue  # Don't care about this if we can't set it.
            if option.long in booleans and option.value == 0:
                repeatable.add(option.long)
            elif hasattr(option.value, '__iter__'):
                repeatable.add(option.long)

    return settable, booleans, repeatable, short_map


def get_env(key, env_prefix, boolean, repeatable):
    """Get one value from environment variable(s).

    :raise KeyError: If option not in environment variables.

    :param str key: Option long name (e.g. --config).
    :param str env_prefix: Variable name prefix from docoptcfg().
    :param bool boolean: Is this a boolean/flag option?
    :param bool repeatable: Is this option repeatable?

    :return: Value to set in the defaults dict. May be int, iter, string, or bool.
    """
    env_name = '{0}{1}'.format(env_prefix, key[2:].replace('-', '_').upper())

    # Handle repeatable non-boolean options (e.g. --file=file1.txt --file=file2.txt).
    if repeatable and not boolean:
        values = list()
        if env_name in os.environ:  # Optional variable not ending with integer.
            values.append(os.environ[env_name])
        for i in range(99):
            env_name_i = '{0}{1}'.format(env_name, i)  # Loop until variable with integer not found.
            if env_name_i not in os.environ:
                break
            values.append(os.environ[env_name_i])
        if not values:
            raise KeyError(env_name)  # Nothing found.
        return values

    if env_name not in os.environ:
        raise KeyError(env_name)

    # Handle repeatable booleans.
    if repeatable and boolean:
        try:
            return int(os.environ[env_name])
        except (TypeError, ValueError):
            return 0

    # Handle the rest.
    if boolean:
        return os.environ[env_name].strip().lower() in ('true', 'yes', 'on', '1')
    return os.environ[env_name]


def values_from_env(env_prefix, settable, booleans, repeatable):
    """Get all values from environment variables.

    :param str env_prefix: Argument from docoptcfg().
    :param iter settable: Option long names available to set by config file.
    :param iter booleans: Option long names of boolean/flag types.
    :param iter repeatable: Option long names of repeatable options.

    :return: Settable values.
    :rtype: dict
    """
    defaults_env = dict()
    for key in settable:
        try:
            defaults_env[key] = get_env(key, env_prefix, key in booleans, key in repeatable)
        except KeyError:
            pass
    return defaults_env


def get_opt(key, config, section, booleans, repeatable):
    """Get one value from config file.

    :raise DocoptcfgFileError: If an option is the wrong type.

    :param str key: Option long name (e.g. --config).
    :param ConfigParser config: ConfigParser instance with config file data already loaded.
    :param str section: Section in config file to focus on.
    :param iter booleans: Option long names of boolean/flag types.
    :param iter repeatable: Option long names of repeatable options.

    :return: Value to set in the defaults dict.
    """
    # Handle repeatable non-boolean options (e.g. --file=file1.txt --file=file2.txt).
    if key in repeatable and key not in booleans:
        return config.get(section, key[2:]).strip('\n').splitlines()

    # Handle repeatable booleans.
    if key in repeatable and key in booleans:
        try:
            return config.getint(section, key[2:])
        except ValueError as exc:
            raise DocoptcfgFileError('Repeatable boolean option "{0}" invalid.'.format(key[2:]), str(exc))

    # Handle non-repeatable booleans.
    if key in booleans:
        try:
            return config.getboolean(section, key[2:])
        except ValueError as exc:
            raise DocoptcfgFileError('Boolean option "{0}" invalid.'.format(key[2:]), str(exc))

    # Handle the rest.
    return str(config.get(section, key[2:]))


def values_from_file(docopt_dict, config_option, settable, booleans, repeatable):
    """Parse config file and read settable values.

    Can be overridden by both command line arguments and environment variables.

    :raise DocoptcfgError: If `config_option` isn't found in docstring.
    :raise DocoptcfgFileError: On any error while trying to read and parse config file.

    :param dict docopt_dict: Dictionary from docopt with environment variable defaults merged in by docoptcfg().
    :param str config_option: Config option long name with file path as its value.
    :param iter settable: Option long names available to set by config file.
    :param iter booleans: Option long names of boolean/flag types.
    :param iter repeatable: Option long names of repeatable options.

    :return: Settable values.
    :rtype: dict
    """
    section = docopt.DocoptExit.usage.split()[1]
    settable = set(o for o in settable if o != config_option)
    config = ConfigParser()
    defaults = dict()

    # Sanity checks.
    if config_option not in docopt_dict:
        raise DocoptcfgError
    if docopt_dict[config_option] is None or not settable:
        return defaults

    # Read config file.
    path = DocoptcfgFileError.FILE_PATH = docopt_dict[config_option]
    try:
        with open(path) as handle:
            if hasattr(config, 'read_file'):
                config.read_file(handle)
            else:
                getattr(config, 'readfp')(handle)
    except Error as exc:
        raise DocoptcfgFileError('Unable to parse config file.', str(exc))
    except IOError as exc:
        raise DocoptcfgFileError('Unable to read config file.', str(exc))

    # Make sure section is in config file.
    if not config.has_section(section):
        raise DocoptcfgFileError('Section [{0}] not in config file.'.format(section))

    # Parse config file.
    for key in settable:
        if config.has_option(section, key[2:]):
            defaults[key] = get_opt(key, config, section, booleans, repeatable)

    return defaults


def docoptcfg(doc, argv=None, env_prefix=None, config_option=None, ignore=None, *args, **kwargs):
    """Pass most args/kwargs to docopt. Handle `env_prefix` and `config_option`.

    :raise DocoptcfgError: If `config_option` isn't found in docstring.
    :raise DocoptcfgFileError: On any error while trying to read and parse config file (if enabled).

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
    docopt_dict = docopt.docopt(doc, argv, *args, **kwargs)
    if env_prefix is None and config_option is None:
        return docopt_dict  # Nothing to do.
    if argv is None:
        argv = sys.argv[1:]
    if ignore is None:
        ignore = ('--help', '--version')
    settable, booleans, repeatable, short_map = settable_options(doc, argv, ignore, kwargs.get('options_first', False))
    if not settable:
        return docopt_dict  # Nothing to do.

    # Handle environment variables defaults.
    if env_prefix is not None:
        defaults = values_from_env(env_prefix, settable, booleans, repeatable)
        settable -= set(defaults.keys())  # No longer settable by values_from_file().
        docopt_dict.update(defaults)

    # Handle config file defaults.
    if config_option is not None:
        defaults = values_from_file(
            docopt_dict,
            short_map.get(config_option, config_option),
            settable,
            booleans,
            repeatable,
        )
        docopt_dict.update(defaults)

    return docopt_dict
