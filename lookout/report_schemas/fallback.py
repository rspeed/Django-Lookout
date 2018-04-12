from .base import ReportSchema


__all__ = ['FallbackReportSchema']



class FallbackReportSchema (ReportSchema):
	""" Catchall fallback. """

	type = 'misc'
	name = "Unknown Incident Report"
	description = "An incident report which didn't match any of the known schemas."

	schema = {'type': 'object'}
