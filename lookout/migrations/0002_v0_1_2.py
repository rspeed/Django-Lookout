from django.db.migrations import Migration as BaseMigration, RunPython, AddField, RenameField, AlterField, AlterModelOptions
from django.db.models import CharField, DateTimeField, TextField, UUIDField
import uuid



def populate_report_uuid (apps, schema_editor):
	"""
	Populates the UUID fields of existing `Report`s.
	This is necessary because the `default` property of a `FormField` will set the same value on every existing row.
	"""

	db_alias = schema_editor.connection.alias
	Report = apps.get_model('lookout', 'Report')

	for report in Report.objects.using(db_alias).all():
		if report.uuid is not None:
			raise ValueError("An existing field has a value for its UUID, which shouldn't be the case during this migration.")

		report.uuid = uuid.uuid4()
		report.save(update_fields=['uuid'])



class Migration(BaseMigration):
	replaces = [
		('lookout', '0002_auto_20171008_2238'),
		('lookout', '0003_auto_20171008_2324'),
		('lookout', '0004_v0_1_1')
	]


	dependencies = [
		('lookout', '0001_initial'),
	]


	operations = [
		# Add a UUID field, populate it, then set it as the primary key
		AddField(
			model_name='report',
			name='uuid',
			field=UUIDField(default=None, primary_key=False, null=True)
		),
		RunPython(populate_report_uuid, RunPython.noop),
		AlterField(
			model_name='report',
			name='created',
			field=DateTimeField(primary_key=False, auto_now_add=True, db_index=True, help_text='When the incident report was submitted.', verbose_name='Submission Time')
		),
		AlterField(
			model_name='report',
			name='uuid',
			field=UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, editable=False),
		),

		AlterField(
			model_name='report',
			name='generated',
			field=DateTimeField(db_index=True, help_text="When the incident occurred.")
		),
		AlterField(
			model_name='report',
			name='body',
			field=TextField(help_text="The contents of the incident report.")
		),

		# Add some more choices
		AlterField(
			model_name='report',
			name='type',
			field=CharField(
				choices=[
					('csp', 'Content Security Policy Report'),
					('legacy_csp', 'Legacy Content Security Policy Report'),
					('hpkp', 'HTTP Public Key Pinning Report'),
					('legacy_hpkp', 'Legacy HTTP Public Key Pinning Report'),
					('misc', 'Unknown Incident Report')
				],
				db_index=True, help_text="The report's category.", max_length=120
			)
		),

		RenameField(
			model_name='report',
			old_name='created',
			new_name='created_time'
		),
		RenameField(
			model_name='report',
			old_name='generated',
			new_name='incident_time'
		),

		AlterModelOptions(
			name='report',
			options={'ordering': ['-incident_time']}
		)
	]
