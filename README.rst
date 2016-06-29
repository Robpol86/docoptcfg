=========
docoptcfg
=========

Love using `docopt <http://docopt.org/>`_ over argparse or `Click <http://click.pocoo.org/>`_? Wish it took care of
environment variables and/or config files?

``docoptcfg`` is a wrapper for ``docopt`` which handles reading configuration data from environment variables and/or an
INI/INF configuration file. You can (1) enable only the environment variable part, (2) only the config file part, (3) or
use both at the same time:

1. ``args = docoptcfg(__doc__, env_prefix='MYAPP_')``
2. ``args = docoptcfg(__doc__, config_option='--config')``
3. ``args = docoptcfg(__doc__, config_option='--config', env_prefix='MYAPP_')``

📖 Full documentation: https://docoptcfg.readthedocs.org

* Python 2.6, 2.7, PyPy, PyPy3, 3.3, 3.4, and 3.5 supported on Linux and OS X.
* Python 2.7, 3.3, 3.4, and 3.5 supported on Windows (both 32 and 64 bit versions of Python).

.. image:: https://img.shields.io/appveyor/ci/Robpol86/docoptcfg/master.svg?style=flat-square&label=AppVeyor%20CI
    :target: https://ci.appveyor.com/project/Robpol86/docoptcfg
    :alt: Build Status Windows

.. image:: https://img.shields.io/travis/Robpol86/docoptcfg/master.svg?style=flat-square&label=Travis%20CI
    :target: https://travis-ci.org/Robpol86/docoptcfg
    :alt: Build Status

.. image:: https://img.shields.io/coveralls/Robpol86/docoptcfg/master.svg?style=flat-square&label=Coveralls
    :target: https://coveralls.io/github/Robpol86/docoptcfg
    :alt: Coverage Status

.. image:: https://img.shields.io/pypi/v/docoptcfg.svg?style=flat-square&label=Latest
    :target: https://pypi.python.org/pypi/docoptcfg
    :alt: Latest Version

Quickstart
==========

Install:

.. code:: bash

    pip install docoptcfg

Changelog
=========

This project adheres to `Semantic Versioning <http://semver.org/>`_.

1.0.2 - 2016-06-28
------------------

Fixed
    * Bug where docoptcfg failed to handle positional arguments with repeating args/opts.

1.0.1 - 2016-01-25
------------------

Fixed
    * setup.py was previously configured for packages, not modules.

1.0.0 - 2016-01-25
------------------

* Initial release.
