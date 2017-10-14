from ..utils import attribute
from .base import ReportSchema



class GenericReportSchema (ReportSchema):
	""" Represents the schema of an Out-of-Band Reporting API incident report. """

	class Meta:
		abstract = True


	@attribute
	@classmethod
	def body_schema (cls):
		return NotImplementedError


	@attribute
	@classmethod
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
