===================
docoptcfg |version|
===================

Love using `docopt <http://docopt.org/>`_ over argparse or `Click <http://click.pocoo.org/>`_? Wish it took care of
environment variables and/or config files?

docoptcfg is a wrapper for docopt which handles reading configuration data from environment variables and/or an INI/INF
configuration file. You can (1) enable only the environment variable part, (2) only the config file part, (3) or use
both at the same time:

1. ``args = docoptcfg(__doc__, env_prefix='MYAPP_')``
2. ``args = docoptcfg(__doc__, config_option='--config')``
3. ``args = docoptcfg(__doc__, config_option='--config', env_prefix='MYAPP_')``

Compatibility
=============

docoptcfg is supported on Linux, OS X, and Windows:

* Python 2.6, 2.7, PyPy, PyPy3, 3.3, 3.4, and 3.5 supported on Linux and OS X.
* Python 2.7, 3.3, 3.4, and 3.5 supported on Windows (both 32 and 64 bit versions of Python).

Simple Example
==============

Here's a simple example of what you can do with docoptcfg. Think of docoptcfg as using configuration files and/or
environment variables to set defaults. Command line arguments will always trump other sources. Environment variables
also trump config files. The order of operations from low to high priority is: **config file -> env var -> args.**

.. code:: python

    #!/usr/bin/env python
    """My little script.

    Usage:
        my_script [options]

    Options:
        -c FILE --config=FILE       Path to INI config file.
        -l FILE --log-file=FILE     Write to this log file.
        -r NUM --runtime=NUM        How long before exiting.
        -t NUM --threads=NUM        Number of threads.
    """

    from docoptcfg import docoptcfg

    print docoptcfg(__doc__, env_prefix='MYAPP_', config_option='--config')

Now let's create a configuration file and name it config.ini:

.. code:: ini

    [my_script]
    log-file = file_config.log
    runtime = 10
    threads = 11

And finally we run it like this:

.. code:: bash

    export MYAPP_LOG_FILE=file_env.log
    export MYAPP_RUNTIME=20
    ./my_script.py -c config.ini -r 30

Our result is:

.. code:: python

    {
        '--config': 'config.ini',
        '--log-file': 'file_env.log',
        '--runtime': '30',
        '--threads': '11',
    }

Project Links
=============

* Documentation: https://robpol86.github.io/docoptcfg
* Source code: https://github.com/Robpol86/docoptcfg
* PyPI homepage: https://pypi.python.org/pypi/docoptcfg

.. toctree::
    :maxdepth: 3
    :caption: General

    install
    usage
    env_vars
    config_files

.. toctree::
    :maxdepth: 1
    :caption: Appendix

    changelog
