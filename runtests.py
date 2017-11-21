#!/usr/bin/env python
import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner



if __name__ == '__main__':
	os.environ['DJANGO_SETTINGS_MODULE'] = 'lookout.tests.test_settings'
	django.setup()

	# Get the test runner class based on the settings
	TestRunner = get_runner(settings)

	# Instantiate the runner and run the tests
	failures = TestRunner().run_tests(['lookout'])

	sys.exit(bool(failures))
