#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
	use_scm_version={'write_to': 'lookout/VERSION.txt'},

	packages=find_packages(exclude=[
		'lookout.tests',
		'lookout.tests.*'
	]),
	package_data={
		'lookout': ['VERSION.txt']
	},

	install_requires=[
		'Django>=1.10',
		'Pygments<3>=2.2',
		'jsonschema<3>=2.6.0',
		'pytz>=2017.2'  # Not provided with Django<=1.10
	],
	setup_requires=[
		'setuptools-scm',
		'wheel'
	],
	extras_require={
		'dev': [
			'codecov',
			'setuptools-scm'
		],
		'docs': [
			'Sphinx>=1.6'
		]
	},
	python_requires='>=3.5',
)
