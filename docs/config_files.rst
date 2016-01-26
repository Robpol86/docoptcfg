.. _config_file:

===================
Configuration Files
===================

When configuration file support is enabled (by specifying ``config_option`` in docoptcfg), Python's native
`configparser`_ module is used to read configuration files. That means only INI/INF-type config files are supported.

An example configuration file is:

.. code:: ini

    [my_script]
    log-file = file_config.log
    runtime = 10
    threads = 11

Below are a few things to keep in mind.

The Basics
==========

Let's get some basics out of the way. When calling ``docoptcfg()`` with the ``config_option`` argument, the value of
that argument should be one of the options defined in your docstring. For example if we've got this docstring:

.. code:: text

    My little script.

    Usage:
        my_script [options]

    Options:
        -c FILE --config=FILE       Path to INI config file.
        -l FILE --log-file=FILE     Write to this log file.
        -r NUM --runtime=NUM        How long before exiting.
        -t NUM --threads=NUM        Number of threads.

Then ``config_option`` should be set to one of those, such as ``config_option='--config'``. You'll need the hyphens.

Another thing to point out is that docoptcfg ignores re-defining configuration files within configuration files. So if
your end user has this:

.. code:: ini

    [my_script]
    config = new_config.ini
    runtime = 10

Then docoptcfg will just ignore the config setting. It will read the rest of the config file like normal.

Lastly, you can combine configuration files and environment variables. So your users can define a configuration file
with ``PREFIX_CONFIG=/path/to/config.ini`` instead of through the command line.

Exception Handling
==================

Unlike environment variables which don't throw any exceptions, configuration file handling may raise two exceptions:

* ``docoptcfg.DocoptcfgError``
* ``docoptcfg.DocoptcfgFileError``

DocoptcfgError
--------------

This one's easy. It's only raised under one scenario: when you (the developer) specifies the wrong option for
``config_option`` when calling docoptcfg(). With the above example docstring, if you do
``docoptcfg(__doc__, config_option='--i-dont-exist')`` then ``DocoptcfgError`` will be raised.

DocoptcfgFileError
------------------

This one may be raised by a mistake on your end-users' part. Be sure to handle this. This is raised on any error that
may come up while attempting to read and parse a config file. Situations include:

* File not found
* Permissions
* Corrupt/binary data instead of text data
* Malformed section formatting
* Missing section
* Non-boolean value for boolean options (valid values are listed in the `configparser documentation`_)

A simple way to handle this is:

.. code:: python

    try:
        CONFIG = docoptcfg(__doc__, config_option='--config')
    except DocoptcfgFileError as exc:
        log.error('Failed reading: %s', str(exc))
        CONFIG = docoptcfg(__doc__)

Section Name
============

docoptcfg will only focus on one section in the config file. The name of that section must match the name of your
program specified in your docstring. The example above has the section named "my_script". Therefore in your docstring
the first word after "Usage:" should match.

Short Names
===========

Like environment variables, only long option names are used. In the example above we've got ``-l FILE --log-file=FILE``
but docoptcfg will only look for ``log-file``.

Flags/Booleans
==============

Flags in config files must be yes, no, on, off, true, false, 1, or 0. More info in the `configparser documentation`_.

Repeating Options
=================

Docopt supports repeating options by specifying an ellipses in the docstring. An example:

.. code:: text

    Test handling of ... options.

    Usage:
        my_script [--config=FILE] [--flag]... [--key=VAL]...

    Options:
        --config=FILE   Path INI config file.
        --flag          Boolean value.
        --key=VAL       Key value value.

In this case, docopt gives you integers for flags (instead of booleans) and lists for key/value options (instead of
strings).

docoptcfg supports this in configuration files as well:

1. Configuration file options for flags are expected to be integers.
2. Configuration file options for key/values can be delimited by newlines.

Here's a quick example:

.. code:: ini

    [my_script]
    key =
        a
        b
        c
    flag = 2

The above is the equivalent of ``my_script --key=a --key=b --key=c --flag --flag``.

.. _configparser: https://docs.python.org/3/library/configparser.html
.. _configparser documentation: https://docs.python.org/3/library/configparser.html#supported-datatypes
