import logging
import json

from datetime import timedelta

from django.db import models
from django.utils import formats
from django.utils.safestring import mark_safe
from django.utils import timezone

from pygments import highlight
from pygments.lexers.data import JsonLexer
from pygments.formatters.html import HtmlFormatter


logger = logging.getLogger(__name__)


__all__ = ['Report']



class ReportManager (models.Manager):
	def create_from_schema (self, report):
		""" Converts a parsed JSON report into a model instance. """

		# Report data as a dictionary
		data = dict(report)

		# Use a static datetime object to make sure `created`, `generated`, and `body['age']` are consistent
		now = timezone.now()

		# Build the model instance
		return self.create(
			created=now,
			type=data['type'],
			# Use the report's `age` property to determine when it was generated
			generated=now - timedelta(milliseconds=data['age']),
			url=data['url'],
			# Store the serialized version
			body=str(report)
		)



class Report (models.Model):
	""" A report filed through the HTTP Reporting API. """

	objects = ReportManager()

	created = models.DateTimeField(auto_now_add=True, primary_key=True)

	type = models.CharField(max_length=120, help_text="The report's category.")
	generated = models.DateTimeField(help_text="The time at which the report was generated.")
	url = models.URLField(help_text="The address of the document or worker from which the report was generated.")
	body = models.TextField(help_text="The contents of the report.")


	def pretty_body (self):
		""" Displays a nicely-formatted version of a the report's body. """
		response = highlight(
			# Reformat the JSON to add whitespace
			json.dumps(json.loads(self.body), sort_keys=True, indent=2),
			JsonLexer(),
			HtmlFormatter(style='colorful', noclasses=True)
		)

		return mark_safe(response)



	class Meta:
		ordering = ['-created']


	def __str__ (self):
		return "{} report from {}".format(self.type.capitalize(), formats.date_format(self.created, 'SHORT_DATETIME_FORMAT'))


