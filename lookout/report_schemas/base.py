from typing import ClassVar, AnyStr

from logging import getLogger
from collections import OrderedDict
import jsonschema

from ..exceptions import UnknownSchemaError


__all__ = ['report_schema_registry', 'ReportSchema']


logger = getLogger(__name__)



class ReportSchemaBase (type):
	""" Base metaclass which adds ``ReportSchema``s to the registry. """

	def __new__(mcs, name, bases, attributes):

		# Create the class object
		new_class = super().__new__(mcs, name, bases, attributes)

		try:
			abstract = attributes['Meta'].abstract
		except (AttributeError, KeyError):
			# The Meta object or abstract property aren't set
			abstract = False

		# Add non-abstract classes to the registry
		if not abstract:
			report_schema_registry.register(new_class)

		return new_class



class ReportSchema (metaclass=ReportSchemaBase):

	class Meta:
		abstract = True


	@property
	def schema (self):
		""" A dictionary representing the JSON schema of a certain type of incident report. """
		raise NotImplementedError()


	@property
	def type (self):
		raise NotImplementedError()


	@property
	def name (self):
		raise NotImplementedError()


	@property
	def description (self):
		raise NotImplementedError()


	def is_valid (self, report_data: AnyStr):
		""" Checks to see if the report data matches the schema. """

		try:
			jsonschema.validate(report_data, self.schema)
		except jsonschema.ValidationError:
			return False
		else:
			return True


	def normalize(self, report_data):
		""" Converts legacy schemas to their generic equivalent. """

		return self, report_data



class ReportSchemaRegistry (OrderedDict):

	def register (self, schema: ClassVar[ReportSchema]) -> ReportSchema:
		schema_instance = schema()
		self[schema_instance.type] = schema_instance

		logger.debug("Registered schema {!r}".format(schema_instance.type))

		return schema_instance


	def get_matching_schema (self, report_data: AnyStr):
		""" Returns the first ``ReportSchema`` class which validates the report data. """

		for name, schema in self.items():
			logger.debug("Trying {}".format(name))

			if schema.is_valid(report_data):
				logger.debug("Validated as {}".format(name))

				return schema

		logger.warning("No schemas matched!")
		raise UnknownSchemaError()


report_schema_registry = ReportSchemaRegistry()
