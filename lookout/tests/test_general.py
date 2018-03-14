import re
from pkg_resources import parse_version

from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from django.apps import apps
from django.core.checks import Warning

import lookout
from lookout.admin import ReportAdmin
from lookout.models import Report



class TestVersion (TestCase):
	def test_known (self):
		self.assertNotEqual(None, lookout.__version__)
		self.assertNotEqual('unknown', lookout.__version__)


	@staticmethod
	def __valid_version (version) -> bool:
		"""
		Ensure that the version number is valid.

		1. Parse the version.
		2. Extract the base version (which removes pre-release cruft).
		3. Make sure it consists of only numbers and dots.
		"""
		try:
			version_parsed = parse_version(version)
		except TypeError:
			return False
		else:
			return bool(re.fullmatch(r'[\d.]+', version_parsed.base_version))


	def test_valid (self):
		""" Checks the value of ``lookout.__version__``. """
		self.assertTrue(self.__valid_version(lookout.__version__))


	def test_from_file (self):
		"""
		Checks the value returned by ``lookout.PackageVersion.from_file``.
		This test will fail if there isn't a VERSION.txt file in the ``lookout`` package directory.
		"""
		version = lookout.PackageVersion.from_file()
		self.assertTrue(self.__valid_version(version), "Didn't get a valid version identifier from 'PackageVersion.from_file'.")


	def test_from_distribution (self):
		"""
		Checks the value returned by ``lookout.PackageVersion.from_distribution``.
		This test will fail if the package isn't installed.
		"""
		version = lookout.PackageVersion.from_distribution()
		self.assertTrue(self.__valid_version(version), "Didn't get a valid version identifier from 'PackageVersion.from_distribution'.")



class TestConfigWarnings (TestCase):
	""" Ensures that ``DjangoLookoutConfig`` is informing Django about configuration issues. """
	def test_warnings (self):
		app = apps.get_containing_app_config(type(self).__module__)

		expected_warnings = [
			Warning(
				"'INVALID_TEST_KEY' is not a valid setting name for Django Lookout.",
				hint="The key must be all-caps and have an equivalent default setting.",
				obj=app
			),
			Warning(
				"'invalid_key_test' is not a valid setting name for Django Lookout.",
				hint="The key must be all-caps and have an equivalent default setting.",
				obj=app
			)
		]
		for expected_warning in expected_warnings:
			self.assertTrue(expected_warning in app.checks)



class MockSuperUser:
	""" Pretends to be a user with all permissions. """
	def has_perm(self, perm):
		return True


class MockRequest:
	""" Pretends to be a Request performed by a superuser. """
	def __init__(self):
		self.user = MockSuperUser()


class TestAdmin (TestCase):
	""" Ensures that the admin behaves as expected. """
	fixtures = ['model_tests/reports']

	ALL_FIELDS = ['body', 'created_time', 'incident_time', 'type', 'url', 'pretty_body']
	DISPLAY_FIELDS = ['created_time', 'incident_time', 'type', 'url', 'pretty_body']


	def setUp (self):
		self.request = MockRequest()

		self.admin = ReportAdmin(Report, AdminSite())

		# Grab the first Report object
		self.report = Report.objects.first()


	def test_fields (self):
		# All fields are assigned to fieldsets
		self.assertEqual(list(self.admin.get_form(self.request).base_fields), [])

		self.assertEqual(list(self.admin.get_fields(self.request)), self.ALL_FIELDS)
		self.assertEqual(list(self.admin.get_fields(self.request, self.report)), self.ALL_FIELDS)


	def test_readonly_fields (self):
		# All fields should be marked as readonly
		self.assertEqual(list(self.admin.get_readonly_fields(self.request, self.report)), self.DISPLAY_FIELDS)


	def test_readonly_post (self):
		self.request.method = 'POST'

		# All admin functions should be read-only, even for a superuser
		self.assertFalse(self.admin.has_add_permission(self.request))
		self.assertFalse(self.admin.has_change_permission(self.request))
		self.assertFalse(self.admin.has_delete_permission(self.request))


	def test_readonly_get (self):
		self.request.method = 'GET'

		# Should be True when the request method is GET, which allows the form to be displayed
		self.assertTrue(self.admin.has_change_permission(self.request))

		# But the rest should still be False
		self.assertFalse(self.admin.has_add_permission(self.request))
		self.assertFalse(self.admin.has_delete_permission(self.request))
