from .base import BaseReportTestCase
from lookout.models import Report



class PythonApiTestCase(BaseReportTestCase):
	""" Tests direct creation of Report objects. """

	def test (self):
		# Create the Report instances from the fixture
		reports = list(Report.objects.create_from_json(self.raw_fixture))

		# Ensures that at least one report was created
		self.assertGreater(len(reports), 0)

		# Test saving the report to the database
		for report in reports:
			with self.subTest(saving=report):
				report.save()

		# Retrieve the reports from the database and verifying that its validity
		for report in reports:
			with self.subTest(fetching=report):
				fetched_report = Report.objects.get(pk=report.pk)

				self.assertEqual(report, fetched_report)



def load_tests(loader, tests, pattern):
	# Start off fresh
	tests = type(tests)()

	# Iterate over the TestCase and load the tests
	for test_case in PythonApiTestCase:
		tests.addTests(loader.loadTestsFromTestCase(test_case))

	return tests
