from os import path

from django.core.urlresolvers import reverse
from django.test import Client, TestCase



class HttpApiTestCase (TestCase):
	""" Tests reporting via the HTTP API endpoint. """

	# TODO add invalid reports
	fixture_files = [
		'hpkp_1.json',
		'csp_1.json',
		'deprecation_1.json',
		'multiple_1.json'
	]
	fixtures = {}


	def setUp (self):
		self.report_url = reverse('lookout:http-report')

		for fixture_file_name in self.fixture_files:
			with open(path.join(path.dirname(__file__), 'fixtures', fixture_file_name), 'r', ) as fixture_file:
				# Read the contents of the fixture file into the fixtures dictionary
				self.fixtures[fixture_file_name] = fixture_file.read()


	def test_path (self):
		self.assertEqual(self.report_url, '/report')


	def test_view (self):
		client = Client()

		for fixture_data in self.fixtures.values():
			response = client.post(self.report_url, data=fixture_data, content_type='application/json')

			# Success!
			self.assertEqual(response.status_code, 200)
