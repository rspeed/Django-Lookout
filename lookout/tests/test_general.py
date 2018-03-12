from pkg_resources import parse_version
from django.test import TestCase
import re

import lookout



class TestVersion (TestCase):
	def test_known (self):
		self.assertNotEqual(None, lookout.__version__)
		self.assertNotEqual('unknown', lookout.__version__)


	def test_valid (self):
		"""
		Ensure that the version number is valid.

		1. Parse the version.
		2. Extract the base version (which removes pre-release cruft).
		3. Make sure it consists of only numbers and dots.
		"""
		self.assertTrue(re.fullmatch(r'[\d.]+', parse_version(lookout.__version__).base_version))
