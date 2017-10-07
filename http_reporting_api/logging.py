from logging import Handler


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
		from .models import Report

		try:
			# Attempt to retrieve the report from the message
			report = record.msg.report
		except AttributeError:
			# Don't do anything if it isn't a ReportMessage object
			# TODO Raise an exception
			return
		else:
			# Create the model instance
			Report.objects.create_from_schema(report)

