from django.db.migrations import Migration as BaseMigration, AlterField
from django.db.models import URLField



class Migration (BaseMigration):
	dependencies = [
		('lookout', '0002_v0_1_2'),
	]


	operations = [
		AlterField(
			model_name='report',
			name='url',
			field=URLField(help_text='The address of the document or worker from which the report was generated.', null=True)
		)
	]
