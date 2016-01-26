"""Sphinx configuration file."""

import time

import sphinx_rtd_theme


# General configuration.
author = '@Robpol86'
copyright = '{}, {}'.format(time.strftime('%Y'), author)
exclude_patterns = ['_build']
master_doc = 'index'
nitpicky = True
project = 'docoptcfg'
release = '1.0.0'
templates_path = ['_templates']
version = release


# Options for HTML output.
html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_title = project
