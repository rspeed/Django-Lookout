#!/usr/bin/env python3

import re
from pkg_resources import parse_version

import django
from django.conf import settings

import lookout


# Configure Django
settings.configure(
	DEBUG=True,
	INSTALLED_APPS=['lookout']
)
django.setup()



# General


extensions = [
	'sphinx.ext.autodoc',
	'sphinx.ext.doctest',
	'sphinx.ext.todo',
	'sphinx.ext.viewcode'
]

templates_path = ['templates']

source_suffix = '.rst'

master_doc = 'index'

project = 'Django Lookout'
copyright = '2017, Rob Speed'
author = 'Rob Speed'

_version = parse_version(str(lookout.__version__))
version = _version.base_version  # Plain version number
release = _version.public  # including alpha/beta/rc tags.

language = None

# List of patterns, relative to source directory, that match files and directories to ignore when looking for source files. This patterns also effect to html_static_path and html_extra_path
exclude_patterns = []

pygments_style = 'sphinx'


# Autodoc Plugin


autodoc_default_flags = [
	'members',
	'undoc-members',
	'show-inheritance'
]


# HTML Output


html_theme = 'sphinx_rtd_theme'

html_theme_options = {}

html_experimental_html5_writer = True

html_logo = 'logo.svg'

html_show_sphinx = False

html_static_path = ['_static']

# Custom sidebar templates, must be a dictionary that maps document names to template names.
html_sidebars = {
	'**': [
		'relations.html',  # needs 'show_related': True theme option to display
		'searchbox.html',
	]
}


INDENT_SIZE = 2

# Fix pydoc's 8-space indentation
def fix_docstring (app, what, name, obj, options, lines):
	indent_pattern = re.compile(r'((?: {8})+)')

	def shift_indent (string):
		match = indent_pattern.match(string)

		if match is not None:
			# The number of 8-space indentations
			indents = match.end() // 8

			return indent_pattern.sub(' ' * indents * INDENT_SIZE, string)

		# If the line isn't indented, return it unmodified
		return string


	# The list has to be updated in-place
	lines[:] = map(shift_indent, lines)



def setup (app):
	app.connect('autodoc-process-docstring', fix_docstring)
