from django.db import migrations, models


class Migration(migrations.Migration):

	dependencies = [
		('lookout', '0001_initial'),
	]

	operations = [
		migrations.RenameField(
			model_name='report',
			old_name='created',
			new_name='created_time'
		),
		migrations.AlterField(
			model_name='report',
			name='created_time',
			field=models.DateTimeField(
				primary_key=True, serialize=False, auto_now_add=True,
				help_text='When the incident report was submitted.',
				verbose_name='Submission Time'
			)
		),
		migrations.RenameField(
			model_name='report',
			old_name='generated',
			new_name='incident_time'
		),
		migrations.AlterField(
			model_name='report',
			name='incident_time',
			field=models.DateTimeField(db_index=True, help_text='When the incident occurred.')
		),
		migrations.AlterField(
			model_name='report',
			name='type',
			field=models.CharField(
				choices=[
					('misc', 'Generic HTTP Reporting API incident report'),
					('csp', 'Content Security Policy Report'),
					('hpkp', 'HTTP Public Key Pinning Report')
				],
				db_index=True,
				help_text="The report's category.",
				max_length=120
			)
		),
		migrations.AlterField(
			model_name='report',
			name='body',
			field=models.TextField(help_text='The contents of the incident report.'),
		),
		migrations.AlterModelOptions(
			name='report',
			options={'ordering': ['-incident_time']},
		),
	]
