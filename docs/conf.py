"""Sphinx configuration file."""

import os
import time
from subprocess import check_output

import sphinx_rtd_theme

SETUP = os.path.join(os.path.dirname(__file__), '..', 'setup.py')


# General configuration.
author = check_output([SETUP, '--author']).strip().decode('ascii')
copyright = '{}, {}'.format(time.strftime('%Y'), author)
master_doc = 'index'
nitpicky = True
project = check_output([SETUP, '--name']).strip().decode('ascii')
release = version = check_output([SETUP, '--version']).strip().decode('ascii')
templates_path = ['_templates']


# Options for HTML output.
html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_title = project
