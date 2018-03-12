#!/usr/bin/env python

""" Script to run tests of a modular Django app without a project. """


if __name__ == '__main__':
	import os
	import sys

	import django
	from django.conf import settings
	from django.test.utils import get_runner


	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lookout.tests.settings')
	django.setup()

	# Get the test runner class based on the settings
	TestRunner = get_runner(settings)

	# Instantiate the runner and run the tests
	failures = TestRunner().run_tests(['lookout'])

	sys.exit(bool(failures))
