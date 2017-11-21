from os import path

from django.test import TestCase

from lookout.models import Report



class PythonApiTestCase (TestCase):
	""" Tests direct creation of Report objects. """

	fixture_files = [
		'hpkp_1.json',
		'csp_1.json',
		'deprecation_1.json',
		'multiple_1.json'
	]
	fixtures = {}


	def setUp (self):
		for fixture_file_name in self.fixture_files:
			with open(path.join(path.dirname(__file__), 'fixtures', fixture_file_name), 'r', ) as fixture_file:
				# Read the contents of the fixture file into the fixtures dictionary
				self.fixtures[fixture_file_name] = fixture_file.read()


	def test (self):
		"""
		Tests a truncated lifecycle for Report objects:

		1. Create the objects from JSON strings.
		2. Save them to the DB.
		3. Use the PK to fetch the record.
		4. Compare the objects.
		"""

		for raw_report in self.fixtures.values():
			reports = Report.objects.create_from_json(raw_report)

			# Save the reports to the DB
			for report in reports:
				report.save()
				fetched_report = Report.objects.get(pk=report.pk)
				self.assertEqual(report, fetched_report)

