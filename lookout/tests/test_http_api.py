from django.urls import reverse
from django.test import Client

from .base import BaseReportTestCase



class HTTPApiTestCase (BaseReportTestCase):
	"""
	Tests reporting via the HTTP API endpoint.

	.. todo:: Add invalid reports
	"""

	def test (self):
		report_url = reverse('lookout:http-report')

		self.assertEqual(report_url, '/report')

		client = Client()
		response = client.post(report_url, data=self.raw_fixture, content_type='application/json')

		self.assertEqual(response.status_code, 200)



def load_tests(loader, tests, pattern):
	# Start off fresh
	tests = type(tests)()

	for test_case in HTTPApiTestCase:
		tests.addTests(loader.loadTestsFromTestCase(test_case))

	return tests
