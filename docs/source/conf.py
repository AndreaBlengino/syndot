# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import subprocess


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'syndot'
copyright = '2024, Andrea Blengino'
author = 'Andrea Blengino'
release = subprocess.run(
    'git describe --tags'.split(), stdout=subprocess.PIPE).stdout.decode(
    'utf-8')

if release.count('-') >= 2:
    release = '-'.join(release.split('-')[:2])


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc']

templates_path = ['_templates']
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']
add_module_names = False
html_title = 'syndot'
