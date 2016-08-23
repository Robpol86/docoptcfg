.. _env_vars:

=====================
Environment Variables
=====================

When environment variables are enabled (by specifying ``env_prefix`` in docoptcfg), there are a few things to keep in
mind.

Short Names
===========

If you've got something like ``-c FILE --config=FILE`` in your docstring, only the ``--config`` part is relevant. Short
option names are ignored in environment variables. So you can't have something like ``PREFIX_C``. Your end users will
need to use ``PREFIX_CONFIG`` instead.

Hyphens
=======

Hyphens in docopt options are underscores in environment variables (e.g. ``--mac-addr`` is ``PREFIX_MAC_ADDR``).

Flags/Booleans
==============

Flags in docopt options  are handled in environment variables as booleans as well. Users will need to set their
environment variable to ``true``, ``yes``, ``on``, or ``1``. These are case insensitive so ``TRUE`` works too. Those
values are interpreted as boolean True while anything else is considered False.

Environment variables set but empty are considered False as well.

So if you've got ``--verbose`` and the user has ``PREFIX_VERBOSE=true``, then you'll have a True value in your returned
dictionary.

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

docoptcfg supports this in environment variables as well:

1. Environment variables for flags are expected to be integers.
2. Environment variables for key/values can be specified multiple times by appending integers from 0 or 1.

For example, the end user may specify ``PREFIX_FLAG=2`` to mimic ``--flag --flag``.

For key/value options they can set ``PREFIX_KEY=one``, ``PREFIX_KEY0=two``, and so on (up to 99 is supported). They can
also start at 1: ``PREFIX_KEY=one``, ``PREFIX_KEY1=two``, ``PREFIX_KEY2=three``. They can even skip the integer-less
variable and do ``PREFIX_KEY0=one``, ``PREFIX_KEY1=two`` and so on. The first variable must start either integer-less or
with 0.

docoptcfg will keep looking for increments until it can't find one. So if the user sets ``PREFIX_KEY0=one``,
``PREFIX_KEY1=two``, and ``PREFIX_KEY3=three``, docoptcfg will only return ``['one', 'two']``.
