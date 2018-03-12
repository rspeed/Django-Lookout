from .generic import GenericReportSchema


__all__ = ['FallbackReportSchema']



class FallbackReportSchema (GenericReportSchema):
	""" Catchall fallback. """

	type = 'misc'
	name = "Unknown Incident Report"
	description = "An incident report which didn't match any of the known schemas."

	schema = {'type': 'object'}
