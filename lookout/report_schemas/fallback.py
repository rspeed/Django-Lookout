from .generic import GenericReportSchema


__all__ = ['FallbackReportSchema']



class FallbackReportSchema (GenericReportSchema):
	""" Catchall fallback. """

	type = 'misc'
	name = "Unknown Incident Report"
	description = ""

	schema = {'type': 'object'}
