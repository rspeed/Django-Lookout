from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

	dependencies = [
		('lookout', '0002_auto_20171008_2238'),
	]

	operations = [
		migrations.AddField(
			model_name='report',
			name='uuid',
			field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, editable=False),
		),
		migrations.AlterField(
			model_name='report',
			name='created_time',
			field=models.DateTimeField(auto_now_add=True, db_index=True, help_text='When the incident report was submitted.', verbose_name='Submission Time'),
		),
	]
