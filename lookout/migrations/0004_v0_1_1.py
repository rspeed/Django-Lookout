from django.db.migrations import Migration as BaseMigration, AlterField
from django.db.models import CharField


# TODO: Convert this to rollup 0002-0004 before v1.0
# Note: The above is only okay because the operation doesn't modify the database.


class Migration (BaseMigration):

	dependencies = [
		('lookout', '0003_auto_20171008_2324'),
	]

	operations = [
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
		)
	]
