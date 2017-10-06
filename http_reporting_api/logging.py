from logging import Handler

from django.apps import apps


__all__ = ['ReportMessage', 'DatabaseLogHandler']



class ReportMessage:
	""" Log message that can contain unserialized report data to be passed to specialized log handlers. """

	msg = "Django HTTP Reporting"
	report = None


	def __init__ (self, msg=None, report=None):
		if msg is not None:
			self.msg = msg

		if report is not None:
			self.report = report



	def __str__ (self):
		""" Returns a plaintext log entry that includes the most important data. """

		return '{}\n{}'.format(self.msg, self.report)



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
