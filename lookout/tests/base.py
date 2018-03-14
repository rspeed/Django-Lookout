from pathlib import Path

from django.test import TestCase
from django.apps import apps



class ReportTestCase (type):
	fixture_dir = None
	fixture_pattern = None


	def __iter__ (cls) -> iter:
		""" Builds subclasses based on report fixture files. """

		# Fixture file directory
		fixture_dir = cls.fixture_dir
		if fixture_dir is None:
			app = apps.get_containing_app_config(cls.__module__)
			fixture_dir = Path(app.path, 'fixtures', 'report_tests')
		else:
			fixture_dir = Path(fixture_dir)

		# Fixture file pattern
		fixture_pattern = cls.fixture_pattern
		if fixture_pattern is None:
			fixture_pattern = '*.json'


		# Create and yield a new subclass for each fixture file
		for fixture_file_name in fixture_dir.glob(fixture_pattern):
			# Reformat the fixture's filename to be a suitable class name
			# Example: foo_bar_1.json -> FooBar1
			name = ''.join(x.capitalize() for x in fixture_file_name.stem.split('_'))

			new_class = type(
				'Test{}'.format(name),
				(cls,),
				{
					'fixture_name': str(fixture_file_name.stem),
					'fixture_file_name': str(fixture_file_name)
				}
			)
			new_class.__module__ = cls.__module__

			yield new_class


class BaseReportTestCase (TestCase, metaclass=ReportTestCase):
	fixture_file_name = None
	""" Path to the actual fixture file. """

	raw_fixture = None
	""" Contents of the fixture file. """


	@classmethod
	def setUpClass(cls):
		super().setUpClass()

		with open(cls.fixture_file_name, 'r') as fixture_file:
			cls.raw_fixture = fixture_file.read()

