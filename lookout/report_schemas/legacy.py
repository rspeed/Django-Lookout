from ..utils import attribute
from .base import ReportSchema



class LegacyReportSchema (ReportSchema):
	""" Parent class for report schemas which can convert reports in a legacy schema into their `GenericReportSchema` counterpart. """

	class Meta:
		abstract = True


	@attribute
	@classmethod
	def generic_class (cls):
		return NotImplementedError


	# Property name of the root object which contains the schema's body
	root_object_name = None


	@attribute
	@classmethod
	def type (cls):
		return 'legacy_{}'.format(cls.generic_class.type)


	@attribute
	@classmethod
	def name (cls):
		return "Legacy {}".format(cls.generic_class.name)


	@attribute
	@classmethod
	def description (cls):
		return "Legacy {}".format(cls.generic_class.description)


	@attribute
	@classmethod
	def body_schema (cls):
		return cls.generic_class.body_schema


	@attribute
	@classmethod
	def schema (cls):
		schema_object = {
			'$schema': 'http://json-schema.org/draft-04/schema#',
			'title': cls.name,
			'description': cls.description,
			'type': 'object'
		}

		if cls.root_object_name is None:
			schema_object.update(cls.body_schema)
		else:
			schema_object.update({
				'required': [cls.root_object_name],
				cls.root_object_name: cls.body_schema
			})

		return schema_object
