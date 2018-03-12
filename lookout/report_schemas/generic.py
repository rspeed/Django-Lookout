from ..utils import classproperty
from .base import ReportSchema



class GenericReportSchema (ReportSchema):
	""" Represents the schema of an Out-of-Band Reporting API incident report. """

	class Meta:
		abstract = True


	@classproperty
	def body_schema (cls):
		"""
		A class attribute containing the sub-schema for the report type's ``body`` property.
		The HTTP Reporting API standardized the root schema of reports, with each type differing only in the value of ``type`` and the structure of ``body``.
		"""
		raise NotImplementedError()


	@classproperty
	def schema (cls):
		return {
			'$schema': "http://json-schema.org/draft-04/schema#",
			'title': cls.name,
			'description': cls.description,
			'type': 'object',
			'required': ['type', 'age', 'url', 'body'],
			'properties': {
				'type': {
					'description': "The type of data the report contains.",
					'type': 'string',
					'enum': [cls.type]
				},
				'age': {
					'description': "The number of milliseconds between the report's timestamp and the current time.",
					'type': 'integer'
				},
				'url': {
					'description': "The URL of the page which triggered the report.",
					'type': 'string',
					'format': 'url'
				},
				'body': {
					**{
						'description': "The contents of the report as defined by the type.",
						'type': 'object'
					},
					**cls.body_schema
				}
			}
		}
