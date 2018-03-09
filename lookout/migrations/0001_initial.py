from django.db import migrations, models


class Migration(migrations.Migration):

	initial = True

	dependencies = []

	operations = [
		migrations.CreateModel(
			name='Report',
			fields=[
				('created', models.DateTimeField(auto_now_add=True, primary_key=True, serialize=False)),
				('type', models.CharField(help_text="The report's category.", max_length=120)),
				('generated', models.DateTimeField(help_text='The time at which the report was generated.')),
				('url', models.URLField(help_text='The address of the document or worker from which the report was generated.')),
				('body', models.TextField(help_text='The contents of the report.'))
			],
			options={
				'ordering': ['-created']
			}
		)
	]
