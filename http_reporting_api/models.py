import logging
import json

from datetime import datetime, timedelta

from django.db import models
from django.utils import formats
from django.utils.safestring import mark_safe

from pygments import highlight
from pygments.lexers.data import JsonLexer
from pygments.formatters.html import HtmlFormatter


logger = logging.getLogger(__name__)


__all__ = ['Report']



class Report (models.Model):
	""" A report filed through the HTTP Reporting API. """

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




	@classmethod
	def create_from_object (cls, report, report_json=None):
		""" Converts a parsed JSON report into a model instance. """

		# Use a static datetime object to make sure `created`, `generated`, and `body['age']` are consistent
		now = datetime.now()

		# Use the report's `age` property to determine when it was generated
		generated = now - timedelta(milliseconds=report['age'])

		# Convert the report object back to JSON if it wasn't provided
		if report_json is None:
			report_json = json.dumps(report)

		# Build the model instance
		self = cls(created=now, type=report['type'], generated=generated, url=report['url'], body=report_json)
		self.save()
		return self
