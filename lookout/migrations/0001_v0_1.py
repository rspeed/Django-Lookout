from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

	replaces = [
		('lookout', '0001_initial'),
		('lookout', '0002_auto_20171008_2238'),
		('lookout', '0003_auto_20171008_2324')
	]

	dependencies = []

	operations = [
		migrations.CreateModel(
			name='Report',
			fields=[
				('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
				('created_time', models.DateTimeField(auto_now_add=True, db_index=True, help_text='When the incident report was submitted.', verbose_name='Submission Time')),
				('type', models.CharField(
					choices=[
						('csp', 'Content Security Policy Report'),
						('legacy_csp', 'Legacy Content Security Policy Report'),
						('hpkp', 'HTTP Public Key Pinning Report'),
						('legacy_hpkp', 'Legacy HTTP Public Key Pinning Report'),
						('misc', 'Unknown Incident Report')
					],
					db_index=True,
					help_text="The report's category.",
					max_length=120
				)),
				('incident_time', models.DateTimeField(db_index=True, help_text='When the incident occurred.')),
				('url', models.URLField(help_text='The address of the document or worker from which the report was generated.')),
				('body', models.TextField(help_text='The contents of the incident report.')),
			],
			options={
				'ordering': ['-incident_time'],
			}
		)
	]
