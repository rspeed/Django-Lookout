from django.db import migrations, models
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


class Migration(migrations.Migration):

	dependencies = [
		('lookout', '0002_auto_20171008_2238'),
	]

	operations = [
		migrations.AddField(
			model_name='report',
			name='uuid',
			field=models.UUIDField(default=None, primary_key=False, null=True)
		),
		migrations.RunPython(populate_report_uuid, migrations.RunPython.noop),

		migrations.AlterField(
			model_name='report',
			name='created_time',
			field=models.DateTimeField(primary_key=False, auto_now_add=True, db_index=True, help_text='When the incident report was submitted.', verbose_name='Submission Time')
		),

		migrations.AlterField(
			model_name='report',
			name='uuid',
			field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, editable=False),
		)
	]
