from django.test import TestCase
from django.apps import apps
from django.db.migrations.executor import MigrationExecutor
from django.db import connection



class TestMigrations (TestCase):
	migrate_from = None
	migrate_to = None


	@classmethod
	def setUpBeforeMigration (cls, migrate_from_apps):
		pass


	@classmethod
	def setUpClass (cls):
		# Get the name of the current Django app
		cls.app_name = apps.get_containing_app_config(cls.__module__).name

		migrate_from = [(cls.app_name, cls.migrate_from)]
		migrate_to = [(cls.app_name, cls.migrate_to)]

		executor = MigrationExecutor(connection)

		# Get the state of django.apps.apps at migrate_from and migrate_to
		migrate_from_apps = executor.loader.project_state(migrate_from).apps
		cls.apps = executor.loader.project_state(migrate_to).apps

		# Run the super-method now to load the fixtures
		super().setUpClass()

		# Reverse the migrations to the starting point (migrate_from)
		executor.migrate(migrate_from)

		# Run the setup
		cls.setUpBeforeMigration(migrate_from_apps)

		# Run the migrations forward to the testing point (migrate_to)
		executor.loader.build_graph()
		executor.migrate(migrate_to)

		# Ready to run some tests!



class UpgradeTo011TestCase (TestMigrations):
	migrate_from = '0001_initial'
	migrate_to = '0002_v0_1_2'

	fixtures = ['model_tests/reports']


	@classmethod
	def setUpBeforeMigration (cls, apps):
		Report = apps.get_model(cls.app_name, 'Report')

		cls.old_pks = [report.created for report in Report.objects.all()]


	def test_uuids_created (self):
		""" Tests that migrated ``Report``s have valid UUIDs. """
		Report = apps.get_model(self.app_name, 'Report')

		# Get all of the reports
		reports = Report.objects.all()

		# At least two records in the database
		self.assertGreaterEqual(len(reports), 2)

		# Make sure the UUIDs were populated
		for report in reports:
			self.assertIsNotNone(report.uuid)
			self.assertNotEqual(report.uuid, '')
			self.assertGreaterEqual(len(str(report.uuid)), 36)


	def test_created_date_values (self):
		""" Tests that migrated ``Report``s can still be accessed based on their former primary key. """
		Report = apps.get_model(self.app_name, 'Report')

		reports = Report.objects.filter(created_time__in=self.old_pks)

		# Make sure they're all still there
		self.assertEqual(len(self.old_pks), len(reports))
