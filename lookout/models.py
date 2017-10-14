import logging
import json
import uuid

from datetime import timedelta

from django.db import models
from django.utils import formats
from django.utils.safestring import mark_safe
from django.utils import timezone

from pygments import highlight
from pygments.lexers.data import JsonLexer
from pygments.formatters.html import HtmlFormatter

from .report_schemas import get_matching_schema, report_schema_registry


logger = logging.getLogger(__name__)


__all__ = ['Report']



class ReportManager (models.Manager):
	def create_from_json (self, report_json):
		""" Converts JSON data into a list of Report instances. """

		logger.debug("Decoding JSON")
		report_datum = json.loads(report_json)

		# Wrap single reports in a list
		if not isinstance(report_datum, list):
			report_datum = [report_datum]

		# Iterate over separate reports
		for report_data in report_datum:
			logger.debug("Attempt to determine the type of report by testing each schema.")

			# Figure out what type of report it is
			schema = get_matching_schema(report_data)

			# Normalize to a generic schema
			schema, report_data = schema.normalize(report_data)

			# Use a static datetime object to make sure `created_time`, `incident_time`, and `body['age']` are consistent
			now = timezone.now()

			# Build the model instance
			yield self.create(
				created_time=now,
				# Use the report's `age` property to determine when the incident occurred
				incident_time=now - timedelta(milliseconds=report_data['age']),
				type=schema.type,
				url=report_data['url'],
				body=json.dumps(report_data)
			)


report_types = [(schema.type, schema.name) for schema in report_schema_registry.values()]


class Report (models.Model):
	""" A report filed through the HTTP Reporting API. """

	objects = ReportManager()

	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	created_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Submission Time", help_text="When the incident report was submitted.")
	incident_time = models.DateTimeField(db_index=True, help_text="When the incident occurred.")
	type = models.CharField(max_length=120, db_index=True, choices=report_types, help_text="The report's category.")
	url = models.URLField(help_text="The address of the document or worker from which the report was generated.")
	body = models.TextField(help_text="The contents of the incident report.")


	class Meta:
		ordering = ['-incident_time']


	def pretty_body (self):
		""" Displays a nicely-formatted version of a the report's body. """
		response = highlight(
			# Reformat the JSON to add whitespace
			json.dumps(json.loads(self.body), sort_keys=True, indent=2),
			JsonLexer(),
			HtmlFormatter(style='colorful', noclasses=True)
		)

		return mark_safe(response)


	@property
	def schema (self):
		return report_schema_registry.get(self.type)


	def __str__ (self):
		""" Something like " """
		return "{} report from {}".format(
			self.schema.name,
			formats.date_format(self.incident_time, 'SHORT_DATETIME_FORMAT')
		)
