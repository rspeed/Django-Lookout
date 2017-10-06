from logging import Handler

from django.apps import apps


__all__ = ['DatabaseLogHandler']



class DatabaseLogHandler (Handler):
	""" Inserts standard reports into the database. """

	def emit (self, record):
		model = apps.get_model('http_reporting_api', 'Report')

		try:
			# Create the model instance
			report = record.msg.report
			model.create_from_object(report.report, report.report_json)
		except AttributeError:
			# Don't do anything if it isn't a ReportMessage object
			# TODO Raise an exception
			return
