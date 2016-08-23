.. _usage:

=============
Usage and API
=============

docoptcfg is pretty easy to use. Its API is similar to docopt's. The only new arguments compared to docopt are
``env_prefix``, ``config_option``, and ``ignore``. There is a pretty table below describing what they do. Any additional
positional/keyword arguments are passed to docopt.docopt().

The return value docoptcfg gives is a dictionary, the same one you'd expect from docopt except the appropriate values
are changed from their defaults based on how your end-user uses your program.

Installation
============

To obtain docoptcfg install the library with pip:

.. code:: bash

    pip install docoptcfg

Keyword Arguments
=================

To repeat from the main page of the documentation, config file option values are overridden by environment variables
which themselves are overridden by command line arguments. Command line arguments are king.

=============== ========================================================================================================
Name            Description/Notes
=============== ========================================================================================================
doc             Required docstring to parse, just like what you pass to docopt.docopt().
argv            Command line arguments to parse, just like what you pass to docopt.docopt().
env_prefix      Enables environment variable parsing if not None (the default).
config_option   Enables config file parsing if not None (the default).
ignore          Ignore setting options via environment variables or config file.
=============== ========================================================================================================

doc (string)
------------

This is the source of truth and defines any environment variable name or config file option. Those names match the long
option names in your docstring.

argv (list)
-----------

If not defined then ``sys.argv[1:]`` is used (just like docopt).

env_prefix (string)
-------------------

This is the environment variable name prefix to use along with long option names. If you've got
``-c FILE --config=FILE`` in your docstring, and you set ``env_prefix=MYAPP_``, then docoptcfg looks for the environment
variable named ``MYAPP_CONFIG``. If you've got something like ``--mac-address`` then docoptcfg will look for
``MYAPP_MAC_ADDRESS``.

config_option (string)
----------------------

This is the long option name in your docstring that specifies a configuration file. Usually it's
``-c FILE --config=FILE`` but you can choose anything you want. For example if you use ``-s FILE --settings=FILE`` then
you'll want to specify ``config_option='--settings'`` or ``config_option='-s'``.

ignore (list)
-------------

This is a list/tuple/set. By default ``--help`` and ``--version`` are ignored. Also ``config_option`` is ignored in
config files (but not environment variables so you can do ``MYAPP_CONFIG`` for example).
