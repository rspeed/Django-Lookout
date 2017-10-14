
__all__ = ['ReportMessage']



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
