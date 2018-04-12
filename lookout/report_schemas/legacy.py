from .base import ReportSchema



class LegacyReportSchema (ReportSchema):
	""" Parent class for report schemas which can convert reports in a legacy schema into their ```GenericReportSchema``` counterpart. """

	class Meta:
		abstract = True


	@property
	def generic_class (self):
		""" The ``GenericReportSchema`` subclass to which this schema normalizes. """
		return NotImplementedError


	root_object_name = None
	""" Property name of the root object which contains the schema's body. """


	@property
	def type (self):
		return 'legacy_{}'.format(self.generic_class.type)


	@property
	def name (self):
		return "Legacy {}".format(self.generic_class.name)


	@property
	def description (self):
		return "Legacy {}".format(self.generic_class.description)


	@property
	def body_schema (self):
		return self.generic_class.body_schema


	@property
	def schema (self):
		schema_object = {
			'$schema': 'http://json-schema.org/draft-04/schema#',
			'title': self.name,
			'description': self.description,
			'type': 'object'
		}

		if self.root_object_name is None:
			schema_object.update(self.body_schema)
		else:
			schema_object.update({
				'required': [self.root_object_name],
				self.root_object_name: self.body_schema
			})

		return schema_object
